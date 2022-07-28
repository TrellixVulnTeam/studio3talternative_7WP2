import paramiko
import sys
from scp import SCPClient
from zipfile import ZipFile
from getpass import getpass
import os
from dotenv import load_dotenv
from pymongo import MongoClient 
import datetime
import csv
class ConnectAutomation:
    def __init__(self,value):
        load_dotenv()
        self.password=value
        print("Begain")

    def unzip_folder(self,zip_folder, destination, pwd):
        """
        Args:
            zip_folder (string): zip folder to be unzipped
            destination (string): path of destination folder
            pwd(string): zip folder password

        """
        with ZipFile(zip_folder) as zf:
            zf.extractall(destination, pwd=pwd.encode())


    def progress4(self,filename, size, sent, peername):
        sys.stdout.write("(%s:%s) %s's progress: %.2f%%   \r" % (peername[0], peername[1], filename, float(sent)/float(size)*100) )


    def install_zip(self):
        try:
            command = "sudo apt install zip -y"
            stdin , stdout, stderr = c.exec_command("sudo apt install zip -y")
            error_output=stderr.read()
            print(result_output)
            if error_output:
                print("Error {}".format(error_output))
        except:
            print("Zip installation failed or already installed") 


    def ssh_connection(self):
        try:
            pemFilePath = os.environ.get('PEM_FILE_PATH'); #input("Please enter server pem file absolute path : ");
            hostName = os.environ.get('SERVER_IP');  #input("Please enter host/ip address : ");
            userName = os.environ.get('USER_NAME'); #input("Please enter server username : ");
            print(pemFilePath)
            k = paramiko.RSAKey.from_private_key_file(pemFilePath)
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print("connecting")
            c.connect(hostname = hostName, username = userName, pkey = k )

            print("connected")

            self.install_zip()

            mongodb_username = os.environ.get('DATABASE_USER') #input("Enter mongodb username : ");
            mongodb_password = os.environ.get('DATABASE_PASSWORD') #input("Enter mongodb password : ");
            mongodb_database = os.environ.get('DATABASE_NAME') #input("Enter mongodb database : ");
            mongodb_host = os.environ.get('DATABASE_HOST') #input("Enter mongodb host : ");
            mongodb_port= os.environ.get('DATABASE_PORT')  #input("Enter mongodb port : ")

            commands = [
                "mongodump --uri=mongodb://{}:{}@{}:{}/{}".format(mongodb_username,mongodb_password,mongodb_host,mongodb_port,mongodb_database),
                "ls",
                "sudo zip -r dump.zip dump"
            ]

            for command in commands:
                print("Executing {}".format(str(command)))
                stdin , stdout, stderr = c.exec_command(command)
                result_output = stdout.read()
                error_output=stderr.read()
                print(result_output)
                if error_output:
                    print("Error {}".format(error_output))

            scp = SCPClient(c.get_transport(), progress4=self.progress4)
            scp.get('dump.zip')  
            print("\n")
            # print("Enter your password")
            # pwd = getpass()
            self.unzip_folder("dump.zip","dump",self.password)
            os.system("mongo {} --eval 'db.dropDatabase()'".format(mongodb_database))
            db_command="mongorestore --db {} --verbose dump/dump/{}".format(mongodb_database,mongodb_database)
            os.system(db_command)
            
        except Exception as e :
            print("Something goes wrong {}".format(str(e)))
        finally:
            c.close()

    def  db_query(self):
        try:
            client = MongoClient("mongodb://localhost:27017/") 
            mydatabase = client[os.environ.get('DATABASE_NAME')]
            mycollection=mydatabase['properties']
            agg_result= mycollection.aggregate([
                        {
                        "$lookup": {
                            "from": "users",
                            "localField": "currentTenant",
                            "foreignField": "_id",
                            "as": "currentTenant"
                        }
                        },
                        {
                        "$lookup": {
                            "from": "users",
                            "localField": "userId",
                            "foreignField": "_id",
                            "as": "landloard"
                        }
                        },
                        {
                        "$unwind": {
                            "path": "$currentTenant",
                            "preserveNullAndEmptyArrays": True
                        }
                        },
                        {"$unwind":"$landloard"},
                        {"$project":{
                            "_id":1,
                            "Address":{
                            "$concat":[
                                "unitNo: ","$address.unitNo", ", ",
                                "buildingNo: ","$address.buildingNo", ", ",
                                "roadNo: ","$address.roadNo", ", ",
                                "blockNo: ","$address.blockNo", ", ",
                                "city: ","$address.city", ", ",
                                "country: ","$address.country"
                            ]
                            },
                            "Property Registration Date":{ "$dateToString": { "format": "%Y-%m-%d", "date": "$createdAt" } },
                            "Landlord Name":"$landloard.fullName",
                            "Landlord Contact #":"$landloard.fullNumber",
                            "Property Name":"$propertyName",
                            "Status":{
                                "$cond": { "if": { "$eq": [ "$occupied", True ] }, "then": "Occupied", "else": "Vacant" }
                            }
                        }},
                        {"$sort":{"_id":1}}
            ]) 
            with open('property.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Property Name", "Address", "Property Registration Date","Landlord Name","Landlord Contact #","Status"])
                for obj in agg_result:
                    writer.writerow([obj["Property Name"], obj["Address"], obj["Property Registration Date"],obj["Landlord Name"],obj["Landlord Contact #"],obj["Status"]])
        except Exception as e:
            print(e)
        finally:
            print("Executed")   




    def  db_query_users(self):
        try:
            client = MongoClient("mongodb://localhost:27017/") 
            mydatabase = client[os.environ.get('DATABASE_NAME')]
            mycollection=mydatabase['users']
            # agg_result= mycollection.aggregate([
            # {"$match":{
            # "userType":{"$in":["MANAGER","LANDLORD"]}    
            # }},
            # {
            #     "$lookup": {
            #     "from": "properties",
            #     "let": {
            #         "userId": "$_id"
            #     },
            #     "pipeline": [
            #         {
            #         "$match": {
            #             "$expr": {
            #             "$and": [
            #                 { "$eq": ["$occupied", True] },
            #                 { "$eq": ["$isApproved", True] },
            #                 { "$eq": ["$isDeleted", False] },
            #                 { "$eq": ["$userId", "$$userId"] }
            #             ],
            #             },
            #         },
            #         },
            #         {"$project":{
            #         "_id":1    
            #         }}
            #     ],
            #     "as": "occupiedProperties",
            #     },
            # },
            # {
            #     "$lookup": {
            #     "from": "properties",
            #     "let": {
            #         "userId": "$_id"
            #     },
            #     "pipeline": [
            #         {
            #         "$match": {
            #             "$expr": {
            #             "$and": [
            #                 { "$eq": ["$occupied", False] },
            #                 { "$eq": ["$isApproved", True] },
            #                 { "$eq": ["$isDeleted", False] },
            #                 { "$eq": ["$userId", "$$userId"] }
            #             ],
            #             },
            #         },
            #         },
            #         {"$project":{
            #         "_id":1    
            #         }}
            #     ],
            #     "as": "vacantProperties",
            #     },
            # },
            # {
            #     "$lookup": {
            #     "from": "maintainencequeries",
            #     "let": {
            #         "ownerId": "$_id"
            #     },
            #     "pipeline": [
            #         {
            #         "$match": {
            #             "$expr": {
            #             "$and": [
            #                 { "$eq": ["$type", 1] },
            #                 { "$eq": ["$ownerId", "$$ownerId"] }
            #             ],
            #             },
            #         },
            #         },
            #         {"$project":{
            #         "_id":1    
            #         }}
            #     ],
            #     "as": "totalMaintainanceRequest",
            #     },
            # },
            # {
            #     "$lookup": {
            #     "from": "users",
            #     "let": {
            #         "parentId": "$_id"
            #     },
            #     "pipeline": [
            #         {
            #         "$match": {
            #             "$expr": {
            #             "$and": [
            #                 { "$eq": ["$parentId", "$$parentId"] },
            #                 { "$eq": ["$userType", "TEAM_MEMBER"] },
            #                 { "$eq": ["$removeByParent", False] },
            #                 { "$eq": ["$blockByParent", False] },
            #             ],
            #             },
            #         },
            #         },
            #         {"$project":{
            #         "_id":1
            #         }}
            #     ],
            #     "as": "totalTeamMembers",
            #     },
            # },
            # {
            #     "$lookup": {
            #     "from": "bankaccounts",
            #     "let": {
            #         "userId": "$_id"
            #     },
            #     "pipeline": [
            #         {
            #         "$match": {
            #             "$expr": {
            #             "$and": [
            #                 { "$eq": ["$userId", "$$userId"] },
            #                 { "$eq": ["$status","Active"] }
            #             ],
            #             },
            #         },
            #         },
            #         {"$project":{
            #         "_id":1
            #         }}
            #     ],
            #     "as": "totalBankAccounts",
            #     },
            # },
            # {
            #     "$lookup": {
            #     "from": "paymentlogs",
            #     "let": {
            #         "propertyOwnerId": "$_id"
            #     },
            #     "pipeline": [
            #         {
            #         "$match": {
            #             "$expr": {
            #             "$and": [
            #                 { "$eq": ["$propertyOwnerId", "$$propertyOwnerId"] },
            #                 { "$gte": ["$createdAt",datetime.datetime(2020,12,1,0,0,0,0)] },
            #                 { "$eq": ["$transactionData.result", "CAPTURED"] },
            #             ],
            #             },
            #         },
            #         },
            #         {"$project":{
            #         "_id":1
            #         }}
            #     ],
            #     "as": "totalInvoicePaidOnlineThisMonth",
            #     },
            # },
            # {"$project":{
            #     "_id":1,
            #     "PhoneNumber":"$fullNumber",
            #     "name":"$fullName",
            #     "type":"$userType",
            #     "RegisterDate":{ "$dateToString": { "format": "%Y-%m-%d", "date": "$createAt" } },
            #     "Status":{ "$cond": { "if": { "$eq": [ "$isApproved", True ] }, "then": "Approved", "else": "Not Approved" }},
            #     "occupiedProperties":{"$size":"$occupiedProperties"},
            #     "vacantProperties":{"$size":"$vacantProperties"},
            #     "totalProperties":{"$add":[{"$size":"$occupiedProperties"},{"$size":"$vacantProperties"}]},
            #     "totalMaintainanceRequest":{"$size":"$totalMaintainanceRequest"},
            #     "totalTeamMembers":{"$size":"$totalTeamMembers"},
            #     "totalBankAccounts":{"$size":"$totalBankAccounts"},
            #     "totalInvoicePaidOnlineThisMonth":{"$size":"$totalInvoicePaidOnlineThisMonth"}    
            # }},
            # {"$sort":{"name":1}}
            # ]) 


            agg_result= mycollection.aggregate([
            {"$match":{
            "userType":{"$in":["MANAGER","LANDLORD"]}    
            }},
            {
                "$lookup": {
                "from": "properties",
                "let": {
                    "userId": "$_id"
                },
                "pipeline": [
                    {
                    "$match": {
                        "$expr": {
                        "$and": [
                            { "$ne": ["$currentTenant", None] },
                            { "$eq": ["$isApproved", True] },
                            { "$eq": ["$isDeleted", False] },
                            { "$eq": ["$userId", "$$userId"] }
                        ],
                        },
                    },
                    },
                    {"$group":{
                       "_id":None,
                       "totalProperty":{"$sum":1},
                       "totalRent":{"$sum":"$rentAmount"}
                    }},
                    {"$project":{
                         "totalProperty":1,
                         "totalRent":1,
                         "avgRent":{ "$cond": { "if": { "$gt": [ "$totalProperty", 0 ] }, "then": {"$trunc":[{ "$divide": ["$totalRent", "$totalProperty" ] },3]}, "else": 0 }},  
                    }}
                ],
                "as": "occupiedProperties",
                },
            },
            
            {"$unwind":{
                "path":"$occupiedProperties",
                "preserveNullAndEmptyArrays":True
             }},
            {"$project":{
                "_id":1,
                "PhoneNumber":"$fullNumber",
                "name":"$fullName",
                "type":"$userType",
                "RegisterDate":{ "$dateToString": { "format": "%Y-%m-%d", "date": "$createAt" } },
                "Status":{ "$cond": { "if": { "$eq": [ "$isApproved", True ] }, "then": "Approved", "else": "Not Approved" }},
                "occupiedProperties":{ "$cond": { "if": { "$gte": [ "$occupiedProperties.totalProperty", 0 ] }, "then": "$occupiedProperties.totalProperty", "else": 0 }},
                "totalRent":{ "$cond": { "if": { "$gte": [ "$occupiedProperties.totalRent", 0 ] }, "then": "$occupiedProperties.totalRent", "else": 0 }},
                "avgRent":{ "$cond": { "if": { "$gte": [ "$occupiedProperties.avgRent", 0 ] }, "then": "$occupiedProperties.avgRent", "else": 0 }},
            }},
            {"$sort":{"name":1}}
            ]) 
            with open('userReports2.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["PhoneNumber","name", "type", "RegisterDate","Status","occupiedProperties","vacantProperties","totalProperties","totalMaintainanceRequest","totalTeamMembers","totalBankAccounts","totalInvoicePaidOnlineThisMonth"])
                for obj in agg_result:
                    writer.writerow([obj["PhoneNumber"],obj["name"], obj["type"], obj["RegisterDate"],obj["Status"],obj["occupiedProperties"],obj["vacantProperties"],obj["totalProperties"],obj["totalMaintainanceRequest"],obj["totalTeamMembers"],obj["totalBankAccounts"],obj["totalInvoicePaidOnlineThisMonth"]])
        except Exception as e:
            print(e)
        finally:
            print("Executed")  


    def  db_query_users_report_two(self):
        try:
            client = MongoClient("mongodb://localhost:27017/") 
            mydatabase = client[os.environ.get('DATABASE_NAME')]
            mycollection=mydatabase['users']
            agg_result= mycollection.aggregate([
            {"$match":{
            "userType":{"$in":["MANAGER","LANDLORD"]}    
            }},
            {
                "$lookup": {
                "from": "properties",
                "let": {
                    "userId": "$_id"
                },
                "pipeline": [
                    {
                    "$match": {
                        "$expr": {
                        "$and": [
                            # { "$ne": ["$currentTenant", None] },
                            { "$eq": ["$isApproved", True] },
                            { "$eq": ["$isDeleted", False] },
                            { "$eq": ["$userId", "$$userId"] }
                        ],
                        },
                    },
                    },
                    {"$group":{
                       "_id":None,
                       "totalProperty":{"$sum":1},
                       "totalRent":{"$sum":"$rentAmount"}
                    }},
                    {"$project":{
                         "totalProperty":1,
                         "totalRent":1,
                         "avgRent":{ "$cond": { "if": { "$gt": [ "$totalProperty", 0 ] }, "then": {"$trunc":[{ "$divide": ["$totalRent", "$totalProperty" ] },3]}, "else": 0 }},  
                    }}
                ],
                "as": "occupiedProperties",
                },
            },
            
            {"$unwind":{
                "path":"$occupiedProperties",
                "preserveNullAndEmptyArrays":True
             }},
            {"$project":{
                "_id":1,
                "PhoneNumber":"$fullNumber",
                "name":"$fullName",
                "type":"$userType",
                "RegisterDate":{ "$dateToString": { "format": "%Y-%m-%d", "date": "$createAt" } },
                "Status":{ "$cond": { "if": { "$eq": [ "$isApproved", True ] }, "then": "Approved", "else": "Not Approved" }},
                "occupiedProperties":{ "$cond": { "if": { "$gte": [ "$occupiedProperties.totalProperty", 0 ] }, "then": "$occupiedProperties.totalProperty", "else": 0 }},
                "totalRent":{ "$cond": { "if": { "$gte": [ "$occupiedProperties.totalRent", 0 ] }, "then": "$occupiedProperties.totalRent", "else": 0 }},
                "avgRent":{ "$cond": { "if": { "$gte": [ "$occupiedProperties.avgRent", 0 ] }, "then": "$occupiedProperties.avgRent", "else": 0 }},
            }},
            {"$sort":{"name":1}}
            ]) 
            with open('userReports2.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["PhoneNumber","name", "type", "RegisterDate","Status","occupiedProperties","vacantProperties","totalProperties","totalMaintainanceRequest","totalTeamMembers","totalBankAccounts","totalInvoicePaidOnlineThisMonth"])
                for obj in agg_result:
                    writer.writerow([obj["PhoneNumber"],obj["name"], obj["type"], obj["RegisterDate"],obj["Status"],obj["occupiedProperties"],obj["vacantProperties"],obj["totalProperties"],obj["totalMaintainanceRequest"],obj["totalTeamMembers"],obj["totalBankAccounts"],obj["totalInvoicePaidOnlineThisMonth"]])
        except Exception as e:
            print(e)
        finally:
            print("Executed")            

    def  db_query_maintainance(self):
        try:
            client = MongoClient("mongodb://localhost:27017/") 
            mydatabase = client[os.environ.get('DATABASE_NAME')]
            print(mydatabase['maintainancereportsdatas'])
            mycollection=mydatabase['maintainancereportsdatas']
            agg_result= mycollection.aggregate([]) 
            with open('maintainance_report.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["owner", "subject", "propertyName","address","assignedToTeamMember","createdAt","resolveDate","ticketNo","generatedBy","status","type","generateFrom","description"])
                for obj in agg_result:
                    print("1")
                    writer.writerow([obj["owner"], obj["subject"], obj["propertyName"],obj["address"],obj["assignedToTeamMember"],obj["createdAt"],obj["resolveDate"],obj["ticketNo"],obj["generatedBy"],obj["status"],obj["type"],obj["generateFrom"],obj["description"]])
        except Exception as e:
            print(e)
        finally:
            print("Executed")        

            
                       

        

        

cl=ConnectAutomation("Rajendra@123")
cl.db_query_users()


       


