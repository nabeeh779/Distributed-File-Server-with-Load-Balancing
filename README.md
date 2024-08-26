# Distributed File Server System

## Overview

This project implements a distributed file server system that allows multiple clients to upload and download files from a server cluster.
The system leverages both multithreading and multiprocessing to efficiently handle multiple clients and distribute the load across several server instances.

## Features

- **File Upload and Download:** Clients can upload and download files from the server cluster.
- **Multithreading:** Each client connection is handled in a separate thread to allow concurrent operations.
- **Multiprocessing:** Multiple server instances handle requests in parallel to balance the load.
- **Load Balancing:** Distributes client requests across server instances using a round-robin approach.

## Architecture

1. **Client:** 
   - Connects to the load balancer to perform file operations (upload/download).

2. **Load Balancer:**
   - Accepts incoming client connections.
   - Distributes requests across multiple server instances using a round-robin algorithm.

3. **Server Instances:**
   - Handle file operations (upload/download).
   - Process client requests concurrently using multithreading and multiprocessing.
