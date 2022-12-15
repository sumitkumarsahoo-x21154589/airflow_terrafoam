import os
from datetime import timedelta

from airflow import DAG
from airflow.contrib.operators.emr_add_steps_operator import EmrAddStepsOperator
from airflow.contrib.operators.emr_create_job_flow_operator import EmrCreateJobFlowOperator
from airflow.contrib.sensors.emr_step_sensor import EmrStepSensor
from airflow.utils.dates import days_ago
from airflow.providers.amazon.aws.hooks.redshift_cluster import RedshiftHook
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator


DAG_ID = os.path.basename(__file__).replace('.py', '')


bucket_name      = 'emrbuckettestsumit'
S3_KEY           = "x21154589_output"
REDSHIFT_TABLE   = "stack_over_flow_survey"

DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False
}

SPARK_STEPS = [
    {
        'Name': 'x21154589_s3_data_etl',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': ['spark-submit','s3://emrbuckettestsumit/x21154589_scripts/spark_s3_in_s3_out.py'],
        },
    }
]
# spark-submit,s3://<bucket>/files/spark-etl-02.py,s3://<bucket>/input,s3://<bucket>/output

JOB_FLOW_OVERRIDES = {
    'Name': 'x21154589-cluster-airflow',
    'ReleaseLabel': 'emr-6.2.0',
    'Applications': [
        {
            'Name': 'Spark'
        },
    ],
    'Instances': {
        'InstanceGroups': [
            {
                'Name': 'Master nodes',
                'Market': 'ON_DEMAND',
                'InstanceRole': 'MASTER',
                'InstanceType': 'm5.xlarge',
                'InstanceCount': 1,
            }
        ],
        'KeepJobFlowAliveWhenNoSteps': False,
        'TerminationProtected': False,
    },
    'VisibleToAllUsers': True,
    'JobFlowRole': 'EMR_EC2_DefaultRole',
    'ServiceRole': 'EMR_DefaultRole',
    'Tags': [
        {
            'Key': 'Environment',
            'Value': 'Development'
        },
        {
            'Key': 'Name',
            'Value': 'Airflow EMR Demo Project'
        },
        {
            'Key': 'Owner',
            'Value': 'Data Analytics Team'
        }
    ]
}

# # start_operator = DummyOperator(task_id="Begin_execution",  dag=dag)
with DAG(
        dag_id=DAG_ID,
        description='Run built-in Spark app on Amazon EMR',
        default_args=DEFAULT_ARGS,
        dagrun_timeout=timedelta(hours=2),
        start_date=days_ago(1),
        schedule_interval='@once',
        tags=['emr'],
) as dag:
    create_emr_cluster = EmrCreateJobFlowOperator(
        task_id='create_job_flow',
        job_flow_overrides=JOB_FLOW_OVERRIDES
    )

    add_steps_to_cluster = EmrAddStepsOperator(
        task_id='add_steps',
        job_flow_id="{{ task_instance.xcom_pull(task_ids='create_job_flow', key='return_value') }}",
        aws_conn_id='aws_default',
        steps=SPARK_STEPS,
    )

    executing_task_and_removing_emr_cluster = EmrStepSensor(
        task_id='watch_step',
        job_flow_id="{{ task_instance.xcom_pull('create_job_flow', key='return_value') }}",
        step_id="{{ task_instance.xcom_pull(task_ids='add_steps', key='return_value')[0] }}",
        aws_conn_id='aws_default',
    )




    # [START howto_transfer_s3_to_redshift]
    transfer_s3_to_redshift = S3ToRedshiftOperator(
                                task_id          = "transfer_s3_to_redshift",
                                redshift_conn_id = 'redshift_default',
                                s3_bucket        = bucket_name,
                                s3_key           = S3_KEY,
                                schema           = "PUBLIC",
                                table            = REDSHIFT_TABLE,
                                copy_options=["csv"]
                            )
   # [END howto_transfer_s3_to_redshift]

    create_emr_cluster >> add_steps_to_cluster >> executing_task_and_removing_emr_cluster >> transfer_s3_to_redshift
 