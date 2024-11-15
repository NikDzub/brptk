document.body.style.backgroundColor = 'yellow';

let int = setInterval(() => {
  window.scroll(0, 400);
  let comments_container = document.querySelector(
    'div[class*="DivCommentListContainer"]'
  );
  let all_comments = document.querySelectorAll(
    // 'div[class*="DivCommentItemContainer"]'
    'div[class*="DivCommentObjectWrapper"]'
  );
  let last_comment = comments_container.lastElementChild;
  last_comment.scrollIntoView();

  let all_img = document.querySelectorAll('img');
  all_img.forEach((i) => {
    i.remove();
  });
  let all_image = document.querySelectorAll('image');
  all_image.forEach((i) => {
    i.remove();
  });

  all_comments.forEach((comment) => {
    if (
      comment.innerHTML.includes('oj5bn5.online') ||
      comment.innerHTML.includes('LOVE YOU') ||
      comment.innerHTML.includes('textrevesumpgasthor') ||
      comment.innerHTML.includes('eed a boyfriend')
    ) {
      console.log('comment found');
      comment.setAttribute('class', 'target');
      comment.style.backgroundColor = 'blue';
      comment
        .querySelector('div[class*=DivLikeContainer]')
        // .querySelector('div[class*=DivLikeWrapper]')
        .setAttribute('class', 'heart_box');
      clearInterval(int);
    } else {
      comment.remove();
    }
  });
}, 1000);

// setTimeout(() => {
//   document.body.style.backgroundColor = 'red';

//   clearInterval(int);
// }, 60000);
// function kk() {
//   let arr = [];
//   let bb = document.querySelectorAll('div[class*="contributor__name-content"]');
//   bb.forEach((e) => {
//     arr.push(e.innerText);
//   });
//   console.log(arr);
// }
