function getProductData() {

    const titleElement =
        document.querySelector(
            "#productTitle"
        );

    const priceElement =
        document.querySelector(
            ".a-price .a-offscreen"
        );

    const ratingElement =
        document.querySelector(
            "span[data-hook='rating-out-of-text']"
        );

    const reviewElement =
        document.querySelector(
            "span[data-hook='total-review-count']"
        );


    return {

        url:
            window.location.href,

        title:
            titleElement
                ? titleElement.innerText.trim()
                : "N/A",

        price:
            priceElement
                ? priceElement.innerText.trim()
                : "N/A",

        rating:
            ratingElement
                ? ratingElement.innerText.trim()
                : "N/A",

        reviews:
            reviewElement
                ? reviewElement.innerText.trim()
                : "N/A"
    };
}


chrome.runtime.onMessage.addListener(

    function (
        message,
        sender,
        sendResponse
    ) {

        if (
            message.action ===
            "getProduct"
        ) {

            sendResponse(
                getProductData()
            );
        }

    }

);