const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
  publicPath: '/static/src/dist/',
  outputDir: path.resolve(__dirname, '../backend/static/src/dist/'),
  filenameHashing: false,
  runtimeCompiler: true,
  devServer: {
    devMiddleware: {
      writeToDisk: true,
    },
  },
  configureWebpack: {
    output: {
      clean: true,
    },
    plugins: [new CleanWebpackPlugin()],
  },
};
