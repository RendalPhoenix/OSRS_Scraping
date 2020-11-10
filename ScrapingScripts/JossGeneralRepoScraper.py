from github import Github
import stscraper as scraper
import pandas as pd
import time
import re

class repoMethod(scraper.GitHubAPI):
    
    @scraper.api_filter(lambda issue: 'pull_request' not in issue)
    @scraper.api('repos/%s/issues', paginate=True, state='closed', labels=['published'])
    def repo_closed_published_issues(self, repo_slug):
        """Get repository closed issues with "published" label, indicating a published JOSS software package"""
        # https://developer.github.com/v3/issues/#list-issues-for-a-repository
        print("getting repo :" +repo_slug+"issues")
        return repo_slug



#github token set up
gh_api =repoMethod("your github token1,your github token2")
jossList = {'Title':[],'IsGithubRepo':[],'RepoUrl':[],'DoiUrl':[],'UpdatedAt':[]}

#index for console message
currentIndex = 0

#get joss-review repo issues
JossAcceptedSubmitsRaw =gh_api.repo_closed_published_issues('openjournals/joss-reviews')

for joss in JossAcceptedSubmitsRaw:

    jossList['Title'].append(joss["title"])
    jossList['UpdatedAt'].append(joss["closed_at"])

    issueBodyText =str(joss["body"])

    #print the issue body text for debugging
    print(issueBodyText)
  
    #regex to find the repository url and corresponding doi url in the issuebody(markdown text)
    #find the text with repository url
    repoPattern1 = re.compile(r"\*\*Repository\:\*\*(.*?) target",re.DOTALL)
    repoResult =re.search(repoPattern1,issueBodyText).group()
    
    #find the text with doi url
    doiPattern1 = re.compile(r"\*\*Archive\:\*\*(.*?) target",re.DOTALL)
    doiResult=re.search(doiPattern1,issueBodyText).group()
    
    #get the url from doi related text
    doiPattern2=re.compile(r"http(.*?)\"",re.DOTALL)
    doiResultFinal=re.search(doiPattern2,doiResult).group()
    doiUrl=doiResultFinal.rstrip('\"')
    jossList['DoiUrl'].append(doiUrl)
 
    #get all repo urls including none github repos
    repoPatternGeneralUrl=re.compile(r"http(.*?)\"",re.DOTALL)   
    generalPatternResult = re.search(repoPatternGeneralUrl,repoResult).group()
   
    #this is the url of the repo, take out the " on the right side
    repoGeneralUrl=generalPatternResult.rstrip('"')  
    jossList['RepoUrl'].append(repoGeneralUrl)
    
    #find all github repos in the joss repo list
    githubRepoPattern =re.compile(r"http(.*?)github\.com\/(.*?)\"",re.DOTALL)
    finalReturnResult = re.search(githubRepoPattern,repoResult)
    if finalReturnResult is None:
        jossList['IsGithubRepo'].append('FALSE')
    else:
        jossList['IsGithubRepo'].append('TRUE')

    #print message for current status in console
    print("//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
    print('title is :'+joss["title"])
    print(currentIndex)
    currentIndex+=1


#write the list to local excel file
DataChart = pd.DataFrame(jossList)
sheetWriter = pd.ExcelWriter('C:\\Users\\Sun\\Desktop\\Joss_General_List_Published.xlsx')
DataChart.to_excel(sheetWriter)
sheetWriter.save()
#print the data chart result when its all done
print(DataChart)
