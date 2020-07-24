# Clone all respositories GitLab
$BaseURL = "<gitlab_repo>"

$PAT = "<personal_token>"
$groups = (iwr "$($BaseURL)/groups?private_token=$($PAT)" | ConvertFrom-Json);

$structure = [System.Collections.ArrayList]@();

$groups.ForEach({ 

    $ID = $_.ID;
    $Group = @{
        GroupID = $_.id;
        GroupName = $_.name;    
        Projects = [System.Collections.ArrayList]@();
    };
    $projects = ((iwr "$($BaseURL)/groups/$ID/projects?private_token=$($PAT)").Content | ConvertFrom-Json)

    $projects.ForEach({
        $Project = @{ 
            ID = $_.id;
            Name = $_.name;
            Repo = [System.Collections.ArrayList]@();
            Languages = ((iwr "$($BaseURL)/projects/$($_.id)/languages?private_token=$($PAT)").Content | ConvertFrom-Json)
            "SSH_URL_TO_REPO" = $_.ssh_url_to_repo
            "HTTP_URL_TO_REPO" = $_.http_url_to_repo
        }
        $Files = (iwr "$($BaseURL)/projects/$($_.id)/repository/tree?private_token=$($PAT)" | ConvertFrom-Json);
        $Repo = @{
            Files = [System.Collections.ArrayList]@();
        }
        $Files.ForEach{
            $Repo.Files.add($_.name);
        }

        $Repo.HaveGitLabFile =  $Repo.Files.Contains(".gitlab-ci.yml");
        $Repo.HaveJenkinsFile = $Repo.Files.Contains("Jenkinsfile");

        $Project.Repo.add($Repo);
        $Group.Projects.add($Project);

    })

    $structure.add($Group);

})

$structure.ForEach({ $_.Projects.ForEach({ git clone $_.HTTP_URL_TO_REPO }) })

# $structure | ConvertTo-Yaml *> /temp/gitlab_structure
