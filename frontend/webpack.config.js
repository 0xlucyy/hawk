const path = require('path')
const nodeExternals = require('webpack-node-externals')

const clientConfigs = {
    entry: './src/app.js',
    mode: 'development',
    output: {
        filename: 'bundle.js',
        publicPath: '/public/',
        path: path.join(__dirname, 'public')
    },
    module: {
        rules: [{
            test: /\.(js|jsx)$/,
            exclude: /(node_modules)/,
            loader: 'babel-loader',
            options: { presets: ["@babel/env"] }
        }]
    },
    devServer: {
        static: path.join(__dirname, 'public/'),
        devMiddleware: {
          publicPath: '/public/'
        },
        port: 3000,
        hot: "only"
    },
    resolve: { extensions: ['*', '.js', '.jsx'] }
}


const serverConfigs = {
    entry: './server/index.js',
    mode: 'development',
    output: {
        filename: 'index.js',
        publicPath: '/dist/',
        path: path.join(__dirname, 'dist')
    },
    module: {
        rules: [{
            test: /\.(js|jsx)$/,
            exclude: /(node_modules)/,
            loader: 'babel-loader',
            options: { presets: ["@babel/env"] }
        }]
    },
    target: 'node',
    externals: [nodeExternals()],
    node: {
        __dirname: false
    }
}

module.exports = [serverConfigs, clientConfigs]