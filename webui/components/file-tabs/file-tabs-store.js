import { createStore } from "/js/AlpineStore.js";

// This store manages open file tabs in the right column file viewer
const model = {
  // Array of open file tabs
  openTabs: [
    {
      id: 1,
      name: "main.py",
      icon: "📄",
      language: "python",
      content: `# main.py
import os
import sys

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()`
    },
    {
      id: 2,
      name: "config.json",
      icon: "📄",
      language: "json",
      content: `{
  "name": "Agent Zero",
  "version": "1.0.0",
  "settings": {
    "theme": "vscode-dark"
  }
}`
    }
  ],
  
  // Currently active tab ID
  activeTabId: 1,
  
  // Counter for generating unique tab IDs
  _nextId: 3,

  // Initialize the store
  init() {
    // Nothing special to initialize
  },

  // Get the currently active tab
  get activeTab() {
    return this.openTabs.find(tab => tab.id === this.activeTabId) || null;
  },

  // Set active tab by ID
  setActiveTab(tabId) {
    const tab = this.openTabs.find(t => t.id === tabId);
    if (tab) {
      this.activeTabId = tabId;
    }
  },

  // Close a tab by ID
  closeTab(tabId) {
    const index = this.openTabs.findIndex(t => t.id === tabId);
    if (index === -1) return;

    // Remove the tab
    this.openTabs.splice(index, 1);

    // If we closed the active tab, switch to another tab
    if (this.activeTabId === tabId) {
      if (this.openTabs.length > 0) {
        // Switch to the previous tab if available, otherwise the next one
        const newIndex = Math.max(0, index - 1);
        this.activeTabId = this.openTabs[newIndex].id;
      } else {
        // No tabs left
        this.activeTabId = null;
      }
    }
  },

  // Open a new tab (or switch to it if already open)
  openTab(file) {
    // Check if tab is already open
    const existingTab = this.openTabs.find(t => t.name === file.name);
    if (existingTab) {
      this.setActiveTab(existingTab.id);
      return;
    }

    // Create new tab
    const newTab = {
      id: this._nextId++,
      name: file.name,
      icon: file.icon || "📄",
      language: file.language || "text",
      content: file.content || ""
    };

    this.openTabs.push(newTab);
    this.setActiveTab(newTab.id);
  },

  // Check if a tab is active
  isTabActive(tabId) {
    return this.activeTabId === tabId;
  },

  // Get file icon based on extension
  getFileIcon(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    const iconMap = {
      'py': '🐍',
      'js': '📜',
      'json': '📋',
      'html': '🌐',
      'css': '🎨',
      'md': '📝',
      'txt': '📄',
      'sh': '⚙️',
      'yml': '⚙️',
      'yaml': '⚙️'
    };
    return iconMap[ext] || '📄';
  }
};

export const store = createStore("fileTabs", model);

