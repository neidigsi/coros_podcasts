# Setting Up the Launch Agent

A **LaunchAgent** is a macOS mechanism that automatically runs scripts when specific conditions are met (e.g., when a USB device is mounted). This allows the podcast sync to run automatically when you connect your Coros watch.

## Installation Steps

### Step 1: Grant System Permissions

Before setting up the launch agent, you need to grant `/usr/bin/python3` the necessary permissions in macOS System Settings:

1. Open **System Settings** → **Privacy & Security**
2. Scroll down and select **Full Disk Access**
3. Click the **+** button to add an application
4. Press **Cmd + Shift + G** to open the "Go to Folder" dialog
5. Enter `/usr/bin` and press **Enter**
6. Select **python3** and click **Open**
7. Confirm the addition

Alternatively, you can grant permissions via Terminal:
```bash
sudo security add-trusted-cert -d -r trustAsRoot -k /Library/Keychains/System.keychain /path/to/cert
```

### Step 2: Create the Launch Agent File

Copy and customize the launch agent template:

```bash
# Copy the template
cp launchagents/launchagent.xml ~/Library/LaunchAgents/coros_podcast.usb.plist
```

### Step 3: Edit the Configuration

Open the file in your preferred editor:

```bash
nano ~/Library/LaunchAgents/coros_podcast.usb.plist
```

**Update the following values:**

```xml
<!-- Replace /PATH/TO/REPO with the actual path to your cloned repository -->
<string>/Users/YOUR_USERNAME/Documents/Repositories/coros_podcasts/scripts/main.py</string>

<!-- Replace /Volumes/PACE 4 with your watch's mount point -->
<string>/Volumes</string>
```

To find your watch's mount point:
```bash
# Connect your watch and identify the mount point
diskutil list
# or
ls -la /Volumes/ | grep -i coros
```

### Step 4: Load the Launch Agent

After saving the file, load the launch agent:

```bash
launchctl load ~/Library/LaunchAgents/coros_podcast.usb.plist
```

### Step 5: Verify Installation

Check if the launch agent is loaded:

```bash
launchctl list | grep podcast
```

You should see output similar to:
```
- 0 podcast.usb.sync
```

## How It Works

The LaunchAgent configuration file (`coros_podcast.usb.plist`) specifies:

- **Label**: Unique identifier for the launch agent (`podcast.usb.sync`)
- **ProgramArguments**: The command to execute (Python interpreter + script path)
- **WatchPaths**: Directory to monitor – when the watch is mounted here, the script runs automatically
- **RunAtLoad**: Whether to run when the agent is loaded
- **StandardOutPath**: Log file for script output (`/tmp/coros_podcast.log`)
- **StandardErrorPath**: Error log file (`/tmp/coros_podcast.err`)

## Troubleshooting

**To unload the launch agent:**
```bash
launchctl unload ~/Library/LaunchAgents/coros_podcast.usb.plist
```

**Check logs for errors:**
```bash
cat /tmp/coros_podcast.log
cat /tmp/coros_podcast.err
```

**Reload after changes:**
```bash
launchctl unload ~/Library/LaunchAgents/coros_podcast.usb.plist
launchctl load ~/Library/LaunchAgents/coros_podcast.usb.plist
```
