const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = (env, argv) => {
  const isProduction = argv.mode === 'production';

  return {
    entry: './src/index.tsx',
    output: {
      path: path.resolve(__dirname, 'dist'),
      filename: isProduction ? '[name].[contenthash].js' : '[name].js',
      publicPath: '/',
      clean: true,
    },
    resolve: {
      extensions: ['.tsx', '.ts', '.jsx', '.js'],
      alias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
    module: {
      rules: [
        {
          test: /\.tsx?$/,
          use: 'ts-loader',
          exclude: /node_modules/,
        },
        {
          test: /\.css$/i,
          use: ['style-loader', 'css-loader', 'postcss-loader'],
        },
        {
          test: /\.(png|jpe?g|gif|svg)$/i,
          type: 'asset/resource',
        },
      ],
    },
    plugins: [
      new HtmlWebpackPlugin({
        template: './public/index.html',
        title: 'Wim Tilburgs - Smart Health AI Consultant',
        meta: {
          viewport: 'width=device-width, initial-scale=1',
          description: 'AI Health Innovation Expert | Diabetes Pioneer | GPT-5 Research',
          keywords: 'Wim Tilburgs, AI health, diabetes, GPT-5, smart health, consultant',
        },
      }),
      new CopyWebpackPlugin({
        patterns: [
          {
            from: 'public/staticwebapp.config.json',
            to: 'staticwebapp.config.json',
          },
        ],
      }),
    ],
    devServer: {
      historyApiFallback: true,
      port: 3000,
      hot: true,
      open: true,
    },
    optimization: {
      splitChunks: isProduction ? {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            chunks: 'all',
          },
        },
      } : false,
    },
  };
};