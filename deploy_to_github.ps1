# ==============================================================================
# GitHub Publishing Automation Script for Student Record Manager
# ==============================================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "      Student Record Manager - GitHub Deployment Helper      " -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

# Ensure PATH has Git and GitHub CLI
$gitPath = "C:\Users\I.Jeevani\AppData\Local\Programs\Git\cmd"
$ghPath  = "C:\Users\I.Jeevani\AppData\Local\Programs\gh\bin"
$pyPath  = "C:\Users\I.Jeevani\AppData\Local\Programs\Python\Python312-arm64"
$env:Path = "$gitPath;$ghPath;$pyPath;$env:Path"

# Check Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Git is not found in PATH." -ForegroundColor Red
    exit 1
}

# Check if git repo is initialized
if (-not (Test-Path ".git")) {
    Write-Host "[+] Initializing Git repository..." -ForegroundColor Yellow
    git init -b main
}

# Set Git user identity if not configured
$gitName = git config user.name
$gitEmail = git config user.email

if (-not $gitName) {
    $authorName = Read-Host "Enter your Git Name (e.g. John Doe)"
    if ($authorName) { git config --global user.name "$authorName" }
    else { git config user.name "Student Record Manager" }
}

if (-not $gitEmail) {
    $authorEmail = Read-Host "Enter your Git / GitHub Email (e.g. john@example.com)"
    if ($authorEmail) { git config --global user.email "$authorEmail" }
    else { git config user.email "student-manager@local" }
}

# Stage and commit
Write-Host "[+] Staging files and creating commit..." -ForegroundColor Yellow
git add .
git commit -m "feat: initial commit - Student Record Manager with regex validation and persistent storage" -q

Write-Host "`nChoose your deployment method:" -ForegroundColor Cyan
Write-Host " [1] Use GitHub CLI ('gh') to automatically create and push repo (Recommended)"
Write-Host " [2] Link to an existing remote GitHub repository URL and push"
$choice = Read-Host "`nEnter option (1 or 2)"

if ($choice -eq "1") {
    # Check if authenticated
    $authStatus = gh auth status 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n[!] You need to log in to GitHub CLI first." -ForegroundColor Yellow
        Write-Host "Running 'gh auth login' now. Follow the on-screen prompts:`n" -ForegroundColor Cyan
        gh auth login
    }

    $repoName = Read-Host "`nEnter repository name (default: student-record-manager)"
    if (-not $repoName) { $repoName = "student-record-manager" }

    Write-Host "`n[+] Creating GitHub repository and pushing code..." -ForegroundColor Green
    gh repo create $repoName --public --source=. --remote=origin --push

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n============================================================" -ForegroundColor Green
        Write-Host "  SUCCESS! Your project has been published to GitHub!        " -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
    }
} elseif ($choice -eq "2") {
    $remoteUrl = Read-Host "`nEnter your GitHub Repository URL (e.g. https://github.com/username/repo.git)"
    if ($remoteUrl) {
        git remote remove origin 2>$null
        git remote add origin $remoteUrl
        git branch -M main
        git push -u origin main
        Write-Host "`n[+] Push completed!" -ForegroundColor Green
    } else {
        Write-Host "[!] Remote URL was empty. Aborting push." -ForegroundColor Red
    }
} else {
    Write-Host "[!] Invalid option selected." -ForegroundColor Yellow
}
