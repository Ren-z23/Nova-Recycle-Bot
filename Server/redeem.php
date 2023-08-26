<!DOCTYPE html>
<html>
<head>
    <title>Redeem Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }

        .items-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
        }

        .item-row {
            display: flex;
            justify-content: center;
            width: 100%;
        }

        .item-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 40%; /* Display two items side by side in a single row */
            margin: 10px;
            text-align: center;
        }

        .item-image {
            width: 150px;
            height: 150px;
            border: 1px solid #ccc;
            border-radius: 8px;
            cursor: pointer;
        }

        .item-label {
            font-size: 16px;
            margin-top: 5px;
        }

        /* Popup styles */
        .popup-container {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 9999;
        }

        .popup-content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        }

        .popup-content h2 {
            margin-top: 0;
        }

        .popup-content p {
            margin-bottom: 10px;
        }

        .popup-close {
            position: absolute;
            top: 10px;
            right: 10px;
            cursor: pointer;
        }

        .redeemed-popup-container {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 9999;
        }

        .redeemed-popup-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        }
        .redeemed-popup-content h2 {
            margin-top: 0;
        }

        .close-button {
            cursor: pointer;
        }
    </style>
    <script>
        function openPopup(itemName, itemCost) {
            document.getElementById('popup-item-name').innerText = itemName;
            document.getElementById('popup-item-cost').innerText = 'Cost: ' + itemCost + ' points';
            document.getElementById('popup').style.display = 'block';
        }

        function closePopup() {
            document.getElementById('popup').style.display = 'none';
        }

        function redeemItem() {
            // Here, you can add the necessary JavaScript code to handle the redemption process
            // For example, you can use AJAX to send a request to the server for redeeming the item
            alert('Item redeemed successfully!');
            closePopup(); // Close the popup after redeeming
        }
        
        function redeemItem() {
            // Here, you can add the necessary JavaScript code to handle the redemption process
            // For example, you can use AJAX to send a request to the server for redeeming the item

            // Show the redeemed popup
            document.getElementById('popup').style.display = 'none'; // Hide the regular popup
            document.getElementById('redeemed-popup').style.display = 'block'; // Show the redeemed popup
        }

        function closeRedeemedPopup() {
            // Close the redeemed popup
            document.getElementById('redeemed-popup').style.display = 'none';
        }
    </script>
</head>
<body>
    <div class="items-container">
        <div class="item-container">
            <img class="item-image" src="F&N 10%.png" alt="F&N 10%.png" onclick="openPopup('F&N 10% Coupon', '100')">
            <div class="item-label">F&N 10% Coupon</div>
        </div>

        <div class="item-container">
            <img class="item-image" src="F&N 20%.png" alt="F&N 20%.png" onclick="openPopup('F&N 20% Coupon', '200')">
            <div class="item-label">F&N 20% Coupon</div>
        </div>

        <div class="item-container">
            <img class="item-image" src="Pokka 10%.png" alt="Pokka 10%.png" onclick="openPopup('Pokka 10% Coupon', '100')">
            <div class="item-label">Pokka 10% Coupon</div>
        </div>

        <div class="item-container">
            <img class="item-image" src="Pokka 20%.png" alt="Pokka 20%.png" onclick="openPopup('Pokka 20% Coupon', '200')">
            <div class="item-label">Pokka 20% Coupon</div>
        </div>



        <!-- Add more items as needed -->

    </div>

    <!-- Popup container -->
    <div class="popup-container" id="popup">
        <div class="popup-content">
            <span class="popup-close" onclick="closePopup()">&times;</span>
            <h2 id="popup-item-name"></h2>
            <p id="popup-item-cost"></p>
            <button onclick="redeemItem()">Redeem</button>
        </div>
    </div>
    
    <div class="redeemed-popup-container" id="redeemed-popup">
        <div class="redeemed-popup-content">
            <h2>Successfully Redeemed!</h2>
            <img src="tick.png" alt="Redeemed Image" width="150" height="150">
            <p>Your item has been successfully redeemed!</p>
            <button class="close-button" onclick="closeRedeemedPopup()">Close</button>
        </div>
    </div>
    
</body>
</html>
