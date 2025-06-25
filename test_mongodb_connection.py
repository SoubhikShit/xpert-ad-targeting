#!/usr/bin/env python3
"""
MongoDB Connection Test Script
This script helps diagnose MongoDB connection issues.
"""

import os
import sys
from pymongo import MongoClient, ServerApi
from dotenv import load_dotenv

def test_mongodb_connection():
    """Test MongoDB connection and diagnose issues."""
    
    print("=" * 60)
    print("MONGODB CONNECTION DIAGNOSTIC TOOL")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    
    print(f"MONGO_URI loaded: {mongo_uri is not None}")
    if mongo_uri:
        print(f"MONGO_URI length: {len(mongo_uri)}")
        # Mask the password for security
        masked_uri = mongo_uri.replace(mongo_uri.split('@')[0].split(':')[-1], '***')
        print(f"MONGO_URI (masked): {masked_uri}")
    else:
        print("❌ MONGO_URI not found in environment variables")
        return False
    
    print("\n" + "=" * 60)
    print("STEP 1: Testing basic connection...")
    print("=" * 60)
    
    try:
        # Create client
        client = MongoClient(mongo_uri, server_api=ServerApi('1'))
        print("✅ MongoClient created successfully")
        
        # Test ping
        ping_result = client.admin.command('ping')
        print(f"✅ Ping successful: {ping_result}")
        
        # List databases
        print("\n📋 Available databases:")
        databases = client.list_database_names()
        for db in databases:
            print(f"  - {db}")
        
        if not databases:
            print("  ⚠️  No databases found (this might be normal for a new cluster)")
        
        print("\n" + "=" * 60)
        print("STEP 2: Testing XpertDB access...")
        print("=" * 60)
        
        # Check if XpertDB exists
        if "XpertDB" in databases:
            print("✅ XpertDB database exists")
            
            # Try to access XpertDB
            try:
                db = client["XpertDB"]
                collections = db.list_collection_names()
                print(f"📋 Collections in XpertDB: {collections}")
                
                if "billing_data" in collections:
                    print("✅ billing_data collection exists")
                    
                    # Try to access billing_data
                    collection = db["billing_data"]
                    count = collection.count_documents({})
                    print(f"📊 Total documents in billing_data: {count}")
                    
                    # Try to find a sample document
                    sample = collection.find_one()
                    if sample:
                        print("✅ Can read from billing_data collection")
                        print(f"📄 Sample document keys: {list(sample.keys())}")
                    else:
                        print("⚠️  billing_data collection is empty")
                        
                else:
                    print("❌ billing_data collection does not exist")
                    print("💡 You may need to create the collection or check the collection name")
                    
            except Exception as db_error:
                print(f"❌ Error accessing XpertDB: {db_error}")
                if "not authorized" in str(db_error).lower():
                    print("💡 This suggests a permissions issue")
                elif "authentication failed" in str(db_error).lower():
                    print("💡 This suggests an authentication issue")
                    
        else:
            print("❌ XpertDB database does not exist")
            print("💡 You may need to create the database or check the database name")
            
            # Try to create the database (this will fail if no permissions)
            try:
                print("\n🔄 Attempting to create XpertDB database...")
                db = client["XpertDB"]
                # Create a test collection to actually create the database
                test_collection = db["test_collection"]
                test_collection.insert_one({"test": "data"})
                test_collection.delete_one({"test": "data"})
                print("✅ Successfully created XpertDB database")
                
                # Now try to create billing_data collection
                billing_collection = db["billing_data"]
                print("✅ Successfully created billing_data collection")
                
            except Exception as create_error:
                print(f"❌ Could not create XpertDB database: {create_error}")
                if "not authorized" in str(create_error).lower():
                    print("💡 You don't have permission to create databases")
                elif "authentication failed" in str(create_error).lower():
                    print("💡 Authentication failed when trying to create database")
        
        print("\n" + "=" * 60)
        print("STEP 3: Testing with sample data...")
        print("=" * 60)
        
        # Try to insert a test document
        try:
            db = client["XpertDB"]
            collection = db["billing_data"]
            
            # Test document
            test_doc = {
                "login_key": "test_key_123",
                "shop_name": "Test Shop",
                "test": True
            }
            
            # Insert test document
            result = collection.insert_one(test_doc)
            print(f"✅ Successfully inserted test document with ID: {result.inserted_id}")
            
            # Find the test document
            found = collection.find_one({"login_key": "test_key_123"})
            if found:
                print("✅ Successfully found test document")
                print(f"📄 Found document: {found}")
            else:
                print("❌ Could not find test document")
            
            # Clean up - remove test document
            delete_result = collection.delete_one({"login_key": "test_key_123"})
            print(f"✅ Cleaned up test document: {delete_result.deleted_count} document(s) deleted")
            
        except Exception as test_error:
            print(f"❌ Error during test operations: {test_error}")
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print("✅ MongoDB connection is working")
        print("✅ Basic authentication is successful")
        print("✅ Can perform database operations")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        
        # Provide specific guidance based on error
        error_str = str(e).lower()
        if "authentication failed" in error_str:
            print("\n💡 AUTHENTICATION ISSUE DETECTED")
            print("Possible solutions:")
            print("1. Check your username and password in the connection string")
            print("2. Verify the user exists in MongoDB Atlas")
            print("3. Check if the user has the correct permissions")
            print("4. Ensure the connection string format is correct")
        elif "bad auth" in error_str:
            print("\n💡 BAD AUTHENTICATION DETECTED")
            print("Possible solutions:")
            print("1. Verify your MongoDB Atlas credentials")
            print("2. Check if the user has access to the cluster")
            print("3. Ensure the connection string is properly formatted")
        elif "connection" in error_str:
            print("\n💡 CONNECTION ISSUE DETECTED")
            print("Possible solutions:")
            print("1. Check your internet connection")
            print("2. Verify the MongoDB Atlas cluster is running")
            print("3. Check if your IP is whitelisted in MongoDB Atlas")
        else:
            print("\n💡 UNKNOWN ERROR")
            print("Please check the error message above for details")
        
        return False
    
    finally:
        try:
            client.close()
            print("\n🔌 Connection closed")
        except:
            pass

if __name__ == "__main__":
    success = test_mongodb_connection()
    if success:
        print("\n🎉 All tests passed! Your MongoDB connection is working correctly.")
    else:
        print("\n❌ Tests failed. Please fix the issues above before running your application.")
        sys.exit(1) 