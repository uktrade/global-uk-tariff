const path = require('path');

module.exports = {
  entry: './src/static/js/filterTable.jsx',
  output: {
    filename: './src/static/js/filterTable.js',
    path: path.resolve(__dirname)
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  }
};
