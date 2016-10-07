function main(params) {

  var commits = param.commits;
  var parameters = {
    text : "The file '" + commits[0].modified + "' modified by '" + commits[0].author.name + "'."
  };

  whisk.invoke({
    name: "/<myNamespace>/mySlack/post",
    parameters: parameters,
    blocking: true,
    next: function(error, activation) {
      whisk.done(undefined, error);
    }
  });

  return whisk.async();
}
