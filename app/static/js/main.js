/*  This is a really annoying thing I had to do to hotfix bootstrap because for some stupid reason, bootstrap refuses to render
    'invalid-feedback' elements without having 'd-block' added to them. Idiocy. This has been a reported bug for a while.
*/
var invalidFeedbackElements = document.getElementsByClassName("invalid-feedback")
for (var i = 0; i < invalidFeedbackElements.length; i++) {
    invalidFeedbackElements[i].classList.add("d-block")
}