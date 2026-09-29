const API =
    "http://127.0.0.1:5000";


let currentProduct = null;

let currentChart = null;


document.addEventListener(
    "DOMContentLoaded",
    loadProduct
);


async function loadProduct() {

    setStatus(
        "Reading product..."
    );


    chrome.tabs.query(
        {
            active: true,
            currentWindow: true
        },

        async function (tabs) {

            const tab = tabs[0];


            if (
                !tab.url ||
                !tab.url.includes(
                    "amazon."
                )
            ) {

                showError(
                    "Open an Amazon product page first."
                );

                return;
            }


            chrome.tabs.sendMessage(

                tab.id,

                {
                    action:
                        "getProduct"
                },

                async function (product) {

                    if (
                        chrome.runtime.lastError
                    ) {

                        showError(
                            "Please refresh the Amazon page and try again."
                        );

                        return;
                    }


                    if (!product) {

                        showError(
                            "Could not read product information."
                        );

                        return;
                    }


                    currentProduct =
                        product;


                    await scrapeFromBackend(
                        product.url
                    );

                }

            );

        }
    );
}


async function scrapeFromBackend(
    url
) {

    setStatus(
        "Fetching product..."
    );


    try {

        const response =
            await fetch(
                `${API}/api/scrape`,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        url: url
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Backend error"
            );

        }


        currentProduct =
            data;


        displayProduct(
            data
        );


        setStatus(
            "Connected"
        );


    } catch (error) {

        showError(
            error.message
        );

    }
}


function displayProduct(
    product
) {

    document.getElementById(
        "loading"
    ).style.display = "none";


    document.getElementById(
        "content"
    ).style.display = "block";


    document.getElementById(
        "productTitle"
    ).textContent =
        product.title;


    document.getElementById(
        "price"
    ).textContent =
        product.price;


    document.getElementById(
        "rating"
    ).textContent =
        product.rating;


    document.getElementById(
        "reviews"
    ).textContent =
        product.reviews;


    const image =
        document.getElementById(
            "productImage"
        );


    if (
        product.image &&
        product.image !== "N/A"
    ) {

        image.src =
            product.image;

    }


    createChart(
        product.history || []
    );


    displayReviews(
        product.reviews_data || []
    );
}


function createChart(
    history
) {

    if (
        !history ||
        history.length === 0
    ) {

        return;
    }


    const canvas =
        document.getElementById(
            "priceChart"
        );


    if (currentChart) {

        currentChart.destroy();

    }


    const labels =
        history.map(
            item => {

                const date =
                    new Date(
                        item.date
                    );

                return date.toLocaleDateString(
                    "en-IN",
                    {
                        month: "short",
                        year: "numeric"
                    }
                );
            }
        );


    const prices =
        history.map(
            item =>
                item.price
        );


    currentChart =
        new Chart(

            canvas,

            {

                type: "line",

                data: {

                    labels: labels,

                    datasets: [

                        {

                            label:
                                "Price",

                            data:
                                prices,

                            tension:
                                0.3,

                            fill:
                                false

                        }

                    ]

                },

                options: {

                    responsive:
                        true,

                    plugins: {

                        legend: {

                            display:
                                false

                        }

                    }

                }

            }

        );
}


function displayReviews(
    reviews
) {

    const container =
        document.getElementById(
            "reviewList"
        );


    container.innerHTML = "";


    if (
        !reviews.length
    ) {

        container.textContent =
            "No reviews found.";

        return;
    }


    reviews.forEach(
        review => {

            const element =
                document.createElement(
                    "div"
                );


            element.className =
                "review";


            element.innerHTML = `

                <div class="review-name">
                    ${escapeHtml(
                        review.reviewer
                    )}
                </div>

                <div class="review-rating">
                    ${escapeHtml(
                        review.rating
                    )}
                </div>

                <div class="review-text">
                    ${escapeHtml(
                        review.text
                    )}
                </div>

            `;


            container.appendChild(
                element
            );

        }
    );
}


function escapeHtml(
    text
) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        text || "";

    return div.innerHTML;
}


document.getElementById(
    "trackButton"
).addEventListener(
    "click",
    () => {

        if (!currentProduct) {

            return;
        }

        setStatus(
            "Product tracked!"
        );

    }
);


document.getElementById(
    "exportButton"
).addEventListener(
    "click",
    async () => {

        if (!currentProduct) {

            return;
        }


        try {

            const response =
                await fetch(
                    `${API}/api/export`,
                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify(
                                currentProduct
                            )

                    }
                );


            const blob =
                await response.blob();


            const url =
                URL.createObjectURL(
                    blob
                );


            const link =
                document.createElement(
                    "a"
                );


            link.href =
                url;


            link.download =
                "amazon-product.csv";


            link.click();


            URL.revokeObjectURL(
                url
            );


        } catch (error) {

            setStatus(
                "Export failed"
            );

        }

    }
);


function setStatus(
    message
) {

    document.getElementById(
        "status"
    ).textContent =
        message;
}


function showError(
    message
) {

    document.getElementById(
        "loading"
    ).textContent =
        message;

    document.getElementById(
        "loading"
    ).style.color =
        "#b91c1c";

}