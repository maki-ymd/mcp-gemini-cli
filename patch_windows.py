#!/usr/bin/env python3
"""
Patch index.ts to add Windows shell support
"""

# Read the original file
with open('index.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the original code block to replace
original = '''  const { command, initialArgs } = geminiCliCommand;
  const commandArgs = [...initialArgs, ...args];

  return new Promise((resolve, reject) => {
    const child = spawn(command, commandArgs, {
      stdio: ["pipe", "pipe", "pipe"],
    });'''

# Define the replacement code
replacement = '''  const { command, initialArgs } = geminiCliCommand;
  const commandArgs = [...initialArgs, ...args];

  // Windows requires shell: true for proper PATH resolution
  // and double-quoted arguments for -p option
  const isWindows = process.platform === "win32";
  const spawnOptions: any = {
    stdio: ["pipe", "pipe", "pipe"],
  };

  if (isWindows) {
    spawnOptions.shell = true;
    // Quote -p argument values on Windows
    for (let i = 0; i < commandArgs.length; i++) {
      if (commandArgs[i] === "-p" && i + 1 < commandArgs.length) {
        // Replace double quotes with single quotes inside the argument
        const escapedArg = commandArgs[i + 1].replace(/"/g, "'");
        // Wrap the entire argument in double quotes
        commandArgs[i + 1] = `"${escapedArg}"`;
      }
    }
  }

  return new Promise((resolve, reject) => {
    const child = spawn(command, commandArgs, spawnOptions);'''

# Replace the content
if original in content:
    content = content.replace(original, replacement)
    # Write the patched file
    with open('index.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Successfully patched index.ts for Windows support")
else:
    print("❌ Original code block not found. File may have been already patched or modified.")
