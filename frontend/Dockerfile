# Build stage
FROM node:18-alpine as build
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy source code and build
COPY . .
RUN npm run build

# Serve stage (Production)
# For local dev via docker-compose, we override the command to run `npm run dev`
FROM node:18-alpine

WORKDIR /app
COPY --from=build /app /app

EXPOSE 3000

# Default to dev server for local docker-compose
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
