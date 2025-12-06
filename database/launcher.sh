#!/bin/bash
set -e

echo "────────────────────────────────────────────"
echo "   🐳  NimbusGuard Service Launcher"
echo "────────────────────────────────────────────"

echo "Preparing host volumes..."
mkdir -p ../data/postgres
mkdir -p ../data/timescaledb
mkdir -p ../data/redis
echo "Host volumes ready."

echo "Checking Docker status..."
if ! docker info > /dev/null 2>&1; then
  echo "Docker is not running! Please start Docker Desktop."
  exit 1
fi
echo "Docker is running."

echo "🚀 Starting containers using docker compose..."
docker compose up -d

echo "────────────────────────────────────────────"
echo "   ✅ All services are up and running!"
echo "   Use 'docker ps' to verify containers."
echo "────────────────────────────────────────────"