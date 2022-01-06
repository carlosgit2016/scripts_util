-- Show databases
USE master;  
GO  
SELECT name, database_id, create_date  
FROM sys.databases ;  
GO  

-- Show tables
SELECT
  *
FROM
  INFORMATION_SCHEMA.TABLES;
GO

-- Show jobs
SELECT job_id, [name] FROM msdb.dbo.sysjobs;

-- Show full history of a job 
EXEC dbo.sp_help_jobhistory_full  
   @job_id='<job_id>',
   @job_name = N'Log_Failed_Logins',
   @step_id=NULL,
   @sql_message_id=NULL,
   @sql_severity=NULL,
   @start_run_date=NULL,
   @end_run_date=NULL,
   @start_run_time=NULL,
   @end_run_time=NULL,
   @minimum_run_duration=NULL,
   @run_status=NULL,
   @minimum_retries=NULL,
   @oldest_first=NULL,
   @server=NULL,
   @mode=NULL,
   @order_by=NULL,
   @distributed_job_history=NULL
GO

-- Create a new user 

CREATE LOGIN user WITH PASSWORD = '<strong_passowrd>';
go
EXEC master..sp_addsrvrolemember @loginame = N'<login_name>', @rolename = N'sysadmin'
go
