#!/bin/bash
set -e

VERSION=$1

if [ -z "$VERSION" ]; then
  echo "❌ Usage: ./release.sh <version>" >&2
  echo "   Example: ./release.sh 1.1.0" >&2
  exit 1
fi

if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "❌ Version must be in semver format (e.g. 1.1.0), got: '$VERSION'" >&2
  exit 1
fi

TAG="v$VERSION"

if git rev-parse "$TAG" >/dev/null 2>&1; then
  echo "❌ Tag $TAG already exists locally" >&2
  exit 1
fi

git tag "$TAG"
git push origin "$TAG"
echo "✅ Released $TAG"
