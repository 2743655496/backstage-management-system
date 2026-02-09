# -----------------------------
# 1. 构建阶段（Node 环境）
# -----------------------------
FROM node:18 AS build

WORKDIR /app

COPY package*.json ./

RUN npm config set registry https://registry.npmmirror.com \
    && npm install

COPY . .

RUN npm run build


# -----------------------------
# 2. 输出阶段（给 nginx 使用）
# -----------------------------
FROM alpine:3.18 AS output

WORKDIR /dist

COPY --from=build /app/dist .
