import os
from datetime import timedelta

from airflow import DAG
from airflow.contrib.operators.emr_add_steps_operator import EmrAddStepsOperator
from airflow.contrib.operators.emr_create_job_flow_operator import EmrCreateJobFlowOperator
from airflow.contrib.sensors.emr_step_sensor import EmrStepSensor
from airflow.utils.dates import days_ago
import boto3
DAG_ID = os.path.basename(__file__).replace('.py', '')

# connection = boto3.client(
#     'emr',
#     region_name='us-east-1',
#     aws_access_key_id='AKIAXLJZTDDBNRIGCZXM',
#     aws_secret_access_key='YDSZbgT9CyhAO/nku3UbsWtc09CvRjwxWWUK3t5Xm',
# )


# aws_default="arn:aws:iam::505316317378:instance-profile/ec2_test_profile"
# emr_default="arn:aws:iam::505316317378:instance-profile/ec2_test_profile"

DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False
    # 'email': ['kviren101@gmail.com'],
    # 'email_on_failure': True,
    # 'email_on_retry': False,
}

SPARK_STEPS = [
    {
        'Name': 'calculate_pi',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': ['/usr/lib/spark/bin/run-example', 'SparkPi', '10'],
        },
    }
]

JOB_FLOW_OVERRIDES = {
    'Name': 'demo-cluster-airflow',
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

with DAG(
        dag_id=DAG_ID,
        description='Run built-in Spark app on Amazon EMR',
        default_args=DEFAULT_ARGS,
        dagrun_timeout=timedelta(hours=2),
        start_date=days_ago(1),
        schedule_interval='@once',
        tags=['emr'],
) as dag:
    cluster_creator = EmrCreateJobFlowOperator(
        task_id='create_job_flow',
        job_flow_overrides=JOB_FLOW_OVERRIDES
    )

    step_adder = EmrAddStepsOperator(
        task_id='add_steps',
        job_flow_id="{{ task_instance.xcom_pull(task_ids='create_job_flow', key='return_value') }}",
        aws_conn_id='aws_default',
        steps=SPARK_STEPS,
    )

    step_checker = EmrStepSensor(
        task_id='watch_step',
        job_flow_id="{{ task_instance.xcom_pull('create_job_flow', key='return_value') }}",
        step_id="{{ task_instance.xcom_pull(task_ids='add_steps', key='return_value')[0] }}",
        aws_conn_id='aws_default',
    )

    cluster_creator >> step_adder >> step_checker




    

# cluster_id = connection.run_job_flow(
#     Name='test_emr_job_boto3',
#     LogUri='s3://kula-emr-test/logs',
#     ReleaseLabel='emr-5.18.0',
#     Applications=[
#         {
#             'Name': 'Spark'
#         },
#     ],
#     Instances={
#         'InstanceGroups': [
#             {
#                 'Name': "Master nodes",
#                 'Market': 'ON_DEMAND',
#                 'InstanceRole': 'MASTER',
#                 'InstanceType': 'm1.xlarge',
#                 'InstanceCount': 1,
#             },
#             {
#                 'Name': "Slave nodes",
#                 'Market': 'ON_DEMAND',
#                 'InstanceRole': 'CORE',
#                 'InstanceType': 'm1.xlarge',
#                 'InstanceCount': 2,
#             }
#         ],
#         'Ec2KeyName': 'Dkan-key-supun',
#         'KeepJobFlowAliveWhenNoSteps': True,
#         'TerminationProtected': False,
#         'Ec2SubnetId': 'subnet-04a2978b7fc0b4606',
#     },
#     Steps=[
#         {
#             'Name': 'file-copy-step',   
#                     'ActionOnFailure': 'CONTINUE',
#                     'HadoopJarStep': {
#                         'Jar': 's3://kula-emr-test/jars/CopyFilesS3-1.0-SNAPSHOT-jar-with-dependencies.jar',
#                         'Args': ['test.xml', 'kula-emr-test', 'kula-emr-test-2']
#                     }
#         }
#     ],
#     VisibleToAllUsers=True,
#     JobFlowRole='EMR_EC2_DefaultRole',
#     ServiceRole='EMR_DefaultRole',
#     Tags=[
#         {
#             'Key': 'tag_name_1',
#             'Value': 'tab_value_1',
#         },
#         {
#             'Key': 'tag_name_2',
#             'Value': 'tag_value_2',
#         },
#     ],
# )

# print ('cluster created with the step...', cluster_id['JobFlowId'])
