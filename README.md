# vCA-Data-Analyses


This is a Python script to analyse the aggregated vCA data provided at the end of each fund. 

The rationale of the script and equations are descibed in this document - https://docs.google.com/document/d/1O3FGv2Zw0AupNF_HJKA7hamGSZfJ-PErrCbNSmPM9hM/edit
(from section 2 - the complex way)

A few manual steps are still required before running the python script. 
1. Download Aggregated vCA file (fund7 file - https://docs.google.com/spreadsheets/d/1ZM3ytXkMB34iSo2LamNxpver-rs9fShnpeNEia-VdBo/edit#gid=1056757524) as a .xlsx or .csv (change code as required, currentely reading from .xlsx)
2. Download the individual vCA's sheets into local machhine. These can be found in the "Veteran Comunity Advisors" tab of the aggregated file (the sheets of the Top 20 vCAs by number of reviews in fund7 is available in this repo under the individual_vcas folder, and can be used for testing)
3. Unfortunately the name of the individual vCA sheets does not match with the name of the vCA, so the currentely these need to be manually matched in a new file called "filenames.csv" (a filename.csv is available in this repo with top 20 vCAs that can be used for testing)

The script will output 4 .csv sheets:
1. A table showing the deviations for each vCA against the weighted averared scores for each assessment - 'aggregated_deviation_analyses.csv'
2. A table with the average deviation calculated for each vCA - 'deviation_summary.csv'
3. The deviation of each vCA grouped by Assessor_ID - "by_assessor.csv"
4. The deviation of each vCA grouped by Idea - "by_idea.csv"
5. 
Currently I am still creating all plots "manually" from Excell. The plan was to use a package like Matplotlib to generate plots automatically, but haven’t had time to implement this as of yet.                                                                                                                              
