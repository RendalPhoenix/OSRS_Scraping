
from github import Github
import stscraper as scraper
import pandas as pd
import time
import re

#output file path for the scraped joss github repo results
outputFilePath='C:\\Users\\Sun\\Desktop\\Joss_Repos_Full_ConSup.xlsx'


#using local excel file to get the repository url and check whether it is a github repo, the local file is the output result of JossGeneralRepoScraper.py
df = pd.read_excel(r'C:\\Users\\Sun\\Desktop\\Joss_General_List_Published.xlsx',sheet_name=0)
rawList = df.to_dict(orient='records')

#set up token for two scrapers
g = Github(login_or_token="your github token",timeout=30,retry=4)
gh_api = scraper.GitHubAPI("your github token")

jossList = {'Title':[],'RepoUrl':[],'DoiUrl':[],'RepoName':[],'StarsCount':[],'Language':[],'RepoHasWiki':[],'AnonContributorsCount':[],'ContributorsCount':[],'OpenIssuesCount':[],'ClosedIssuesCount':[],'ForksCount':[],'OpenPullRequestsCount':[],'ClosedPullRequestsCount':[],'CommitsCount':[],'UpdatedAt':[],'CreatedAt':[],'Description':[],'Topics':[]}
currentIndex = 0

for element in rawList:

    if str(element['IsGithubRepo']) == 'True':
        title = str(element['Title']).lstrip('[REVIEW]: ')
        jossList['Title'].append(title)        
        doiUrl = str(element['DoiUrl'])
        jossList['DoiUrl'].append(doiUrl)
        repoSlugUrl=str(element['RepoUrl'])
        jossList['RepoUrl'].append(repoSlugUrl)
        
        #strip the string to get the correct repo slugs
        repoSlugRaw=repoSlugUrl+'*'
        topDomainPattern =re.compile(r"github\.com\/(.*?)\*")
        repoSlugExtra=re.search(topDomainPattern,repoSlugRaw).group()
        repoSlug=repoSlugExtra.rstrip('*')
        gitPattern =re.compile(r"\.git")
        gitsearch =re.search(gitPattern,repoSlug)
        if gitsearch is None:
            findsimpleslug = repoSlug.lstrip("github\..").lstrip('com').lstrip('\./').rstrip('/')
        else:
            findsimpleslug = repoSlug.lstrip("github\..").lstrip('com').lstrip('\./').rstrip("git").rstrip(".")
        slugtoprocess = findsimpleslug+'/'
        slugPattern=re.compile(r"(.*?)\/(.*?)\/")
        simpleslug=re.search(slugPattern,slugtoprocess).group()
        repoSlugFinal = simpleslug.rstrip("\./")         
        print(repoSlugFinal)

        if gh_api.project_exists(repoSlugFinal):
            repodetail =g.get_repo(repoSlugFinal)
            jossList['CreatedAt'].append(repodetail.created_at)
            jossList['RepoName'].append(repoSlugFinal)
            jossList['StarsCount'].append(repodetail.stargazers_count)
            jossList['RepoHasWiki'].append(repodetail.has_wiki)
            jossList['Language'].append(repodetail.language)
            jossList['AnonContributorsCount'].append(repodetail.get_contributors(anon='true').totalCount)
            jossList['ContributorsCount'].append(repodetail.get_contributors().totalCount)
            jossList['OpenIssuesCount'].append(repodetail.open_issues_count)
            jossList['ClosedIssuesCount'].append(repodetail.get_issues(state='closed').totalCount)
            jossList['ForksCount'].append(repodetail.forks_count)
            jossList['Topics'].append(repodetail.get_topics())
            jossList['UpdatedAt'].append(repodetail.updated_at)
            jossList['Description'].append(repodetail.description)
            jossList['CommitsCount'].append(repodetail.get_commits().totalCount)
            jossList['OpenPullRequestsCount'].append(repodetail.get_pulls().totalCount)
            jossList['ClosedPullRequestsCount'].append(repodetail.get_pulls(state='closed').totalCount)
        else:
            jossList['CreatedAt'].append('RETRACTED')
            jossList['RepoName'].append(repoSlugFinal)
            jossList['StarsCount'].append('RETRACTED')
            jossList['RepoHasWiki'].append('RETRACTED')
            jossList['Language'].append('RETRACTED')    
            jossList['ContributorsCount'].append('RETRACTED')
            jossList['AnonContributorsCount'].append('RETRACTED')
            jossList['OpenIssuesCount'].append('RETRACTED')
            jossList['ClosedIssuesCount'].append('RETRACTED')   
            jossList['ForksCount'].append('RETRACTED')
            jossList['Topics'].append('RETRACTED')
            jossList['UpdatedAt'].append('RETRACTED')
            jossList['Description'].append('RETRACTED')
            jossList['CommitsCount'].append('RETRACTED')
            jossList['OpenPullRequestsCount'].append('RETRACTED')  
            jossList['ClosedPullRequestsCount'].append('RETRACTED')  


    #print debug messages in console
    print("////////////////////////////////////-------------------------/////////////////////////////////")
    print(repoSlugFinal)
    print(currentIndex)
    currentIndex+=1

    #enable sleep if token limitation is exceeded

    #if currentIndex ==500:
    #    print('sleepingn now for 1800s')
    #    print(time.localtime)
    #    time.sleep(1800)

DataChart = pd.DataFrame(jossList)
writer = pd.ExcelWriter(outputFilePath)
DataChart.to_excel(writer)
writer.save()
print(DataChart)
