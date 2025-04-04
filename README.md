# Reddit Rules to Norms using LLM's

## Introduction

This project aims to leverage Reddit rules from various subreddits to establish obligations, prohibitions, and permissions expressed in Normative Programming Language (NPL). Instead of manually analyzing the rules, we will use **Large Language Models (LLMs)** to achieve this automation. The end goal is to compile these rules and use LLMs to interpret and classify them.

## Table of Contents

- [Reddit Rules to Norms using LLM's](#reddit-rules-to-norms-using-llms)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Section 01: Collecting Rules from Subreddits](#section-01-collecting-rules-from-subreddits)
    - [Step 1: Creating a Developer Application](#step-1-creating-a-developer-application)
    - [Step 2: Setting up the Environment Variables](#step-2-setting-up-the-environment-variables)
    - [Step 3: Testing the API Connection](#step-3-testing-the-api-connection)
    - [Step 4: Fetching Rules](#step-4-fetching-rules)
      - [a. Automated Fetching - `fetching_reddit_rules.py`](#a-automated-fetching---fetching_reddit_rulespy)
      - [b. Manual Fetching - `fetching_reddit_manually.py`](#b-manual-fetching---fetching_reddit_manuallypy)
    - [Step 5: Combining the Rules](#step-5-combining-the-rules)
  - [Project Structure](#project-structure)
  - [Usage Instructions](#usage-instructions)
  - [Caution](#caution)

---

## Section 01: Collecting Rules from Subreddits

### Step 1: Creating a Developer Application

To interact with the Reddit API using PRAW, you need to create a developer application on Reddit:
- Visit: [Reddit Apps](https://www.reddit.com/prefs/apps)
- Click **Create App** or **Create Another App**.
- Fill in the required details.
- Note down the **Client ID** and **Client Secret**.

### Step 2: Setting up the Environment Variables

Once you have your credentials, create a `.env` file in your project directory with the following structure:

```
CLIENT_ID="your Client_ID"
CLIENT_SECRET="your Client_Secret"
USER_AGENT="my_reddit_bot/1.0 by u/yourRedditUsername"
REDDIT_AGENT="MyRuleScraper/1.0 by u/yourRedditUsername"
```

> **Caution:** Keep the `.env` file hidden and do not upload it to public repositories, as it contains sensitive information.

### Step 3: Testing the API Connection

You can test your API connection by running the `reddit.py` script. It should display the top posts from the `Python` subreddit if everything is configured correctly.

### Step 4: Fetching Rules

#### a. Automated Fetching - `fetching_reddit_rules.py`
- This script randomly fetches rules from 10 subreddits with the following criteria:
  - More than **500k members**.
  - Not marked as **NSFW**.

```python
if subreddit.over18:
    continue  # Skip NSFW
if subreddit.subscribers < 500_000:
    continue  # Skip if under 500k subscribers
if count >= 10:
    break  # Stop after 10 subreddits to avoid banning
```

- The script logs each explored subreddit in `explored_subreddits.txt` to avoid duplicate fetching.

#### b. Manual Fetching - `fetching_reddit_manually.py`
- This script allows you to specify subreddits manually by editing the `subreddits` list:

```python
subreddits = ["datascience", "MachineLearning", "Python"]
```

- All fetched rules are saved as JSON files in the `Rules` folder.

### Step 5: Combining the Rules

The `combine_rules.py` script aggregates all the JSON files from the `Rules` folder into a single JSON file structured as follows:

```json
{
    "subreddit": "name_of_subreddit",
    "subscribers": "number_of_subscribers",
    "rules": [
        {
            "Rule_title": "Title of the rule",
            "description": "Details",
            "kind": "Different kind of rules"
        }
    ]
}
```

---

## Project Structure
```
.
├── fetching_reddit_rules.py
├── fetching_reddit_manually.py
├── combine_rules.py
├── reddit.py
├── Rules/
├── explored_subreddits.txt
├── .env
├── requirements.txt
└── README.md
```

## Usage Instructions
1. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create .env File:** Follow the structure provided in [Step 2](#step-2).

3. **Run Scripts:**
- Test API connection: `python reddit.py`
- Fetch rules automatically: `python fetching_reddit_rules.py`
- Fetch rules manually: `python fetching_reddit_manually.py`
- Combine rules: `python combine_rules.py`

## Caution
Ensure your `.env` file is included in your `.gitignore` file to avoid exposing your credentials. Never upload sensitive information to public repositories.

---


