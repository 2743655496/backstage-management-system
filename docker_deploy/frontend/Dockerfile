# -----------------------------
# 1. 构建阶段（Node 环境）
# -----------------------------
FROM node:18 AS build

WORKDIR /app

COPY package*.json ./

#注意更换为你网速最快的源
RUN npm config set registry https://registry.npmmirror.com \
    && npm install
#RUN npm config set registry https://mirrors.huaweicloud.com/repository/npm/ \
#    && npm install

COPY . .

RUN npm run build


# -----------------------------
# 2. 输出阶段（给 nginx 使用）
# -----------------------------
FROM alpine:3.18 AS output

WORKDIR /dist

COPY --from=build /app/dist .
