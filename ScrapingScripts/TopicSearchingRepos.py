from github import Github
import pandas as pd
import time

#set up github token for PyGithub
g = Github("your github token")

topicForIndexing ='scientific-software'
#topicForIndexing ='computational-science'
#topicForIndexing ='simulation-framework'
#topicForIndexing ='biological-simulations'
#topicForIndexing ='scientific-computing'



# search github repositories with topic labels
repositories = g.search_repositories(query='topic:'+topicForIndexing)
newlist ={'IndexTopic':[],'RepoUrl':[],'RepoName':[],'StarsCount':[],'Language':[],'RepoHasWiki':[],'ContributorsCount':[],'OpenIssuesCount':[],'ClosedIssuesCount':[],'ForksCount':[],'OpenPullRequestsCount':[],'ClosedPullRequestsCount':[],'CommitsCount':[],'updated_at':[],'Description':[],'Topics':[]}
currentIndex = 0
for repo in repositories:
    newlist['RepoName'].append(repo.full_name)
    print(repo.full_name)
    repodetail =g.get_repo(repo.full_name)
    newlist['RepoUrl'].append(repodetail.html_url)
    newlist['StarsCount'].append(repodetail.stargazers_count)
    newlist['RepoHasWiki'].append(repodetail.has_wiki)
    newlist['IndexTopic'].append(topicForIndexing)
    print(repodetail.stargazers_count)
    newlist['Language'].append(repodetail.language)
    newlist['ContributorsCount'].append(repodetail.get_contributors().totalCount)
    newlist['OpenIssuesCount'].append(repodetail.open_issues_count)
    newlist['ClosedIssuesCount'].append(repodetail.get_issues(state='closed').totalCount)
    newlist['ForksCount'].append(repodetail.forks_count)
    newlist['Topics'].append(repodetail.get_topics())
    newlist['updated_at'].append(repodetail.updated_at)
    newlist['Description'].append(repodetail.description)
    newlist['CommitsCount'].append(repodetail.get_commits().totalCount)
    newlist['OpenPullRequestsCount'].append(repodetail.get_pulls().totalCount)
    newlist['ClosedPullRequestsCount'].append(repodetail.get_pulls(state='closed').totalCount)

    #check PR merged status, this is a really slow method, highly time consuming
            #repoPulls =repodetail.get_pulls(state='closed')
            #mergedCount = 0
            #for repoPull in repoPulls:
            #    #if repoPull.merged:
            #    #    mergedCount +=1
            #    mergedCount+=repoPull.merged
            #    print(mergedCount)

            #newlist['MergedPullRequestsCount'].append(mergedCount)


    #print messages for console debugging
    print(repo.full_name)
    print(currentIndex)
    if currentIndex ==350:
        print('sleepingn now for 1800s')
        print(time.localtime)
        time.sleep(1800)

    currentIndex+=1


Mychart = pd.DataFrame(newlist)
#local file path to write the excel file
writer = pd.ExcelWriter('C:\\Users\\Sun\\Desktop\\'+topicForIndexing+'.xlsx')
Mychart.to_excel(writer)
writer.save()
print(Mychart)