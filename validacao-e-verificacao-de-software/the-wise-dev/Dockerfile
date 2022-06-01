FROM node:14
WORKDIR /app
COPY ./src ./src
COPY ./tsconfig-build.json .
COPY ./tsconfig.json .
COPY ./package.json .
RUN npm install -g typescript
RUN npm install --save-dev @types/node
RUN npm install --only=prod
RUN npm run build-docker
EXPOSE 8000
RUN chown -R node /app
USER node
CMD ["npm", "start"]