# Snipe-IT Docker Network Connection Fix Guide

## Problem Description

The original deployment encountered a network connection error when trying to pull the PHP base image from Docker Hub:

```
failed to solve: failed to fetch oauth token: Post "https://auth.docker.io/token": dial tcp 162.220.12.226:443: connectex: A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond.
```

## Root Cause Analysis

1. **Network Connectivity Issues**: The error indicates that Docker cannot connect to Docker Hub to download the `php:8.2-fpm-alpine` base image.
2. **Custom Build Approach**: The original configuration uses a custom Dockerfile that builds from scratch, which requires downloading multiple base images and packages.
3. **Geographic Location**: Users in certain regions (especially China) may experience connectivity issues with Docker Hub.

## Solutions Provided

### Solution 1: Official Pre-built Image (Recommended)

**File**: `docker-compose.official.yml`

- Uses the official `snipe/snipe-it` pre-built image
- No custom building required
- Fastest and most reliable deployment
- Follows official documentation recommendations

**Advantages**:
- No network issues with base image downloads
- Faster deployment
- Official support and updates
- Proven stability

### Solution 2: Custom Build with Network Fixes

**Files**: `Dockerfile.fixed` and `docker-compose.fixed.yml`

- Uses Alibaba Cloud mirror for Docker images
- Configured with Chinese package mirrors
- Maintains custom build capability

**Network Fixes Applied**:
- Base image: `registry.cn-hangzhou.aliyuncs.com/library/php:8.2-fpm-alpine`
- Alpine packages: `mirrors.aliyun.com`
- Composer packages: `mirrors.aliyun.com/composer/`
- NPM packages: `registry.npmmirror.com`

### Solution 3: Original Configuration (Fallback)

**Files**: `docker-compose.yml` and `Dockerfile.custom`

- Keeps the original custom build approach
- Can be used if network issues are resolved
- Requires stable connection to Docker Hub

## Deployment Options

### Quick Start (Recommended)

1. Run the fixed deployment script:
   ```cmd
   deploy_snipeit_fixed.bat
   ```

2. Select option 1 (Official pre-built image) for the fastest deployment

### Manual Deployment

#### Option 1: Official Image
```cmd
docker-compose -f docker-compose.official.yml up -d
```

#### Option 2: Fixed Custom Build
```cmd
docker-compose -f docker-compose.fixed.yml up -d --build
```

#### Option 3: Original Custom Build
```cmd
docker-compose up -d --build
```

## Additional Network Troubleshooting

If you continue to experience network issues:

1. **Check Docker Desktop Settings**:
   - Ensure Linux containers are enabled
   - Check proxy settings if behind corporate firewall

2. **Configure Docker Registry Mirrors**:
   - Add registry mirrors in Docker Desktop settings
   - Use local or regional mirrors

3. **Firewall and Proxy Settings**:
   - Check Windows Firewall settings
   - Configure proxy settings if required

4. **DNS Configuration**:
   - Try using different DNS servers (8.8.8.8, 1.1.1.1)
   - Flush DNS cache: `ipconfig /flushdns`

## File Structure

```
├── docker-compose.yml              # Original configuration
├── docker-compose.official.yml     # Official pre-built image (recommended)
├── docker-compose.fixed.yml        # Custom build with network fixes
├── Dockerfile.custom               # Original custom Dockerfile
├── Dockerfile.fixed                # Fixed custom Dockerfile with mirrors
├── deploy_snipeit.bat             # Original deployment script
├── deploy_snipeit_fixed.bat       # Fixed deployment script with options
└── NETWORK_FIX_GUIDE.md           # This guide
```

## Support

If you continue to experience issues:

1. Check Docker logs: `docker-compose logs -f`
2. Verify network connectivity: `ping docker.io`
3. Test with different deployment options
4. Consider using a VPN if in a restricted network environment

## Recommendations

1. **For Production**: Use the official pre-built image (Solution 1)
2. **For Development**: Use the fixed custom build (Solution 2) if you need customizations
3. **For Troubleshooting**: Start with the official image and then move to custom builds if needed

The official pre-built image is the most reliable option as it eliminates the need to download and build multiple components during deployment.

