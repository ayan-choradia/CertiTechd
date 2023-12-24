const ayantest = artifacts.require("ayantest");

/*
 * uncomment accounts to access the test accounts made available by the
 * Ethereum client
 * See docs: https://www.trufflesuite.com/docs/truffle/testing/writing-tests-in-javascript
 */
contract("ayantest", function (/* accounts */) {
  it("should assert true", async function () {
    await ayantest.deployed();
    return assert.isTrue(true);
  });
});
