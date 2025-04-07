# 🌊 **Leaky: Telegram Leak Detection System**

---

## 🌐 **Context and Purpose**
In today's digital age, data breaches and leaks are a growing concern. Malicious actors often share stolen credentials, usernames, and other sensitive information in public or private forums, including Telegram groups. These leaks can harm individuals, organizations, and communities.

**Leaky** was developed as a tool to **help individuals and organizations identify if their usernames, emails, or other identifiers appear in leaked logs**. By automating the process of downloading and searching through these logs, users can take proactive steps to secure their accounts and mitigate potential risks.

---

### ⚖️ **Ethical Use**
This system is designed to be used **ethically and responsibly**:
- ✅ **For personal or organizational security**: Use it to check if your own credentials or those of your organization have been leaked.
- ✅ **To protect others**: Help friends, family, or colleagues identify potential leaks and secure their accounts.

**⚠️ Disclaimer**:  
This system is not intended to promote or facilitate the consumption, distribution, or misuse of leaked data. **Use it at your own risk.** The developer does not condone unethical behavior, and any misuse of this tool is solely the responsibility of the user.

---

## 🛠️ **How the System Works**

The system consists of **two Telegram bots**:
1. 🤖 **Downloader Bot**: Handles all file management tasks, including downloading logs, listing files, checking free disk space, and removing logs by name.
2. 🔍 **Search Bot**: Allows users to search for specific terms (e.g., usernames, emails) within the downloaded logs and manage a watchlist of usernames.

---

### 📂 **File Naming Convention**
The logs downloaded by the Downloader Bot follow a specific naming convention. For example:
- A file named `TXT_AL13N - 1.txt` forwarded to the bot will be saved as `log_1.txt` in the system's directory.

Here’s an example of the content in a log file (`log_1.txt`):
```
https://test1.com:test@test.com:test1pass
https://test2.com:test@test.com:test2pass
https://test3.com:test@test.com:test3pass
https://test4.com:test@test.com:test4pass
https://test5.com:test@test.com:test5pass
```

---

## 🚀 **How to Use Leaky**

### **1. Setting Up the Bots**
- **Downloader Bot**:
  - Configure the bot with your Telegram API credentials (`API_ID`, `API_HASH`, and `PHONE_NUMBER`).
  - Set the `CHANNEL_ID` to the Telegram group/channel where logs are forwarded.
  - The bot will automatically download files and save them in the specified directory (`LOG_PATH`).

- **Search Bot**:
  - Configure the bot with your Telegram Bot Token (`TOKEN`).
  - Set the `LOG_DIR` to the directory where the logs are stored.
  - The bot allows users to register usernames, search for terms, and receive alerts when new logs are detected.

---

### **2. Using the Downloader Bot**
The Downloader Bot is responsible for managing all file-related tasks:
- **Downloading Logs**: Forward a file (e.g., `TXT LOG ALIEN - 1.txt`) from the Telegram group to the bot. The bot will:
  1. Save the file in the `LOG_PATH` directory with a new name (e.g., `log_1.txt`).
  2. Notify you when the file is successfully saved.
- **Listing Files**: Use the `/files` command to list all downloaded logs and their sizes.
- **Checking Free Disk Space**: Use the `/space` command to check the available disk space on the server.
- **Removing Logs**: Use the `/remove <filename>` command to delete a specific log by its name.

---

### **3. Using the Search Bot**
The Search Bot is responsible for searching logs and managing a watchlist:
- **Commands**:
  - `/start`: Displays a list of available commands.
  - `/register <username>`: Add a username to the watchlist.
  - `/remove <username>`: Remove a username from the watchlist.
  - `/list`: List all registered usernames.
  - `/search <term>`: Search for a specific term (e.g., username, email) in the logs.

- **Example Workflow**:
  1. Register a username: `/register myusername`.
  2. Search for a term: `/search myusername`.
  3. If the term is found, the bot will send you the results in a text file.

---

### **4. Automated Alerts**
- The Search Bot periodically checks for new logs in the `LOG_DIR`.
- If a new log is detected, the bot will:
  1. Notify you about the new log.
  2. Search for registered usernames in the new log.
  3. Send alerts if any usernames from the watchlist are found.

**⏰ Note**: The automated alerts are scheduled to run daily at night (e.g., 2:00 AM UTC) to ensure minimal disruption and to allow sufficient time for processing large logs and multiple usernames.  
You can adjust the time in the bot's code (`bot.py`) if necessary, depending on your timezone and usage patterns. For example, if you are in UTC-5, you might set the time to `9:00 PM UTC` to align with your local night hours.

---

## 📌 **Important Notes**
1. **Log File Management**:
   - Logs are stored in the `LOG_PATH` directory. Ensure this directory has sufficient storage space.
   - Regularly clean up old logs to avoid excessive storage usage.

2. **Security**:
   - Keep your API credentials and bot tokens secure.
   - Do not share sensitive information with unauthorized users.

3. **Ethical Responsibility**:
   - Use this system only for ethical purposes, such as protecting yourself or others from potential harm.
   - Do not use this system to exploit or misuse leaked data.

---

## 🏁 **Conclusion**
**Leaky** provides a powerful way to identify potential leaks and take proactive measures to secure accounts. By automating the process of downloading and searching logs, it saves time and effort while promoting cybersecurity awareness.

**⚠️ Remember**: Always use this tool responsibly and ethically. The developer is not responsible for any misuse of the system.

---