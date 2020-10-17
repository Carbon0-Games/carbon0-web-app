module.exports = {
    entry: {
        frontend: './react_leaderboard/src/index.js',
    },
    output: {
        filename: 'main.js',
        path: __dirname + '/static/js/'
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader"
          }
        },
        {
          test: /\.(png|svg|jpg|gif)$/,
          loader: 'url-loader',
        },
      ]
    }
  }