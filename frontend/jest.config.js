module.exports = {
  preset: '@vue/cli-plugin-unit-jest',
  transformIgnorePatterns: ["node_modules/(?!axios)/"],
  moduleNameMapper: {
    '\\.(css|less)$': 'identity-obj-proxy',
  },
};
