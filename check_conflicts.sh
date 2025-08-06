#!/bin/bash

echo "🔍 Conflict Detection and Resolution Tool"
echo "========================================"

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 Current branch: $CURRENT_BRANCH"

# Fetch latest main
echo "📡 Fetching latest main branch..."
git fetch origin main

# Check for potential conflicts
echo "🔍 Checking for potential merge conflicts..."

# Create a temporary merge to see conflicts
echo "🧪 Simulating merge with main..."
git merge origin/main --no-commit --no-ff 2>&1 | tee merge_output.txt

# Check if there are conflicts
if grep -q "CONFLICT" merge_output.txt; then
    echo "⚠️  CONFLICTS DETECTED!"
    echo ""
    echo "📋 Conflicted files:"
    git status --porcelain | grep "^UU\|^AA\|^DD" || git diff --name-only --diff-filter=U
    
    echo ""
    echo "🔧 To resolve conflicts:"
    echo "1. Edit the conflicted files"
    echo "2. Remove conflict markers (<<<<<<< ======= >>>>>>>)"
    echo "3. Choose the secure version (environment variables)"
    echo "4. Run: git add ."
    echo "5. Run: git commit"
    
    # Abort the merge for now
    git merge --abort
    echo "🔄 Merge aborted - conflicts need manual resolution"
else
    echo "✅ No conflicts detected!"
    echo "🎉 Your branch can be merged cleanly"
    # Abort the test merge
    git merge --abort 2>/dev/null || true
fi

# Clean up
rm -f merge_output.txt

echo ""
echo "🚀 Ready for Pull Request creation!"
