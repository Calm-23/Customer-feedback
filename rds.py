import boto3 as boto
import MySQLdb
client = boto.client('rds')


# Creating RDS Instance
response = client.create_db_instance(
    DBName='feedback',
    AllocatedStorage=5,
    DBInstanceClass='db.t2.micro',
    DBInstanceIdentifier='mysqldb',
    Engine='MySQL',
    MasterUserPassword='password',
    MasterUsername='username',
)
print("MySQL instance created....")
print("Waiting for RDS instance to start....")

waiter = client.get_waiter('db_instance_available')
waiter.wait(DBInstanceIdentifier='mysqldb')
print("RDS instance is available.")

response = client.describe_db_instances(
    DBInstanceIdentifier='mysqldb',
)

endpoint = response['DBInstances'][0]['Endpoint']['Address']

print("RDS DNS: %s" %endpoint)


# #Inserting table

# ENDPOINT=endpoint
# PORT="3306"
# USR="username"
# REGION="us-east-2"
# DBNAME="feedback"
# os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

# conn = mysql.connector.connect(
# 	host='mysqldb.c3pg7tvyvrqq.us-east-1.rds.amazonaws.com', 
# 	port=3306, 
# 	database='mysqldb', 
# 	user='username', passwd='password')
#                                                                                                                     conn = mysql.connector.connect(host='customercare.cc04bxcxpc5e.ap-south-1.rds.amazonaws.com', port=3306, database='customercare', user='customercare', passwd='hello123world')
# cur = conn.cursor()
# cur.execute("CREATE TABLE user(username varchar(100),password varchar(100))")
# cur.execute("CREATE TABLE compaints(username varchar(100)complain varchar(1000))")