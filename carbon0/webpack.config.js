module.exports = {
    entry: {
        frontend: './react_leaderboard/src/index.js',
    },
    output: {
        path: __dirname + '/static/js/',
        filename: 'leaderboard.js'
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
          test: /\.css$/,
          use: ["style-loader", "css-loader"],
        },
        {
          test: /\.(png|svg|jpg|gif)$/,
          loader: 'url-loader',
        },
      ]
    }
  }