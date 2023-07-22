<!DOCTYPE html>
<html>

<head>
    <title>Main Page</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
        }

        #navigation-panel {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 60px;
            background-color: #333;
            padding: 10px;
            box-sizing: border-box;
            display: flex;
            align-items: center;
        }

        #navigation-panel img {
            height: 40px;
            cursor: pointer;
            border-radius: 50%;
            /* Make the profile image circular */
            overflow: hidden;
            /* Hide any overflow caused by border-radius */
        }

        #navigation-panel-redeem {
            right: 0px;
        }

        #token-iframe {
            position: absolute;
            top: 60px;
            /* height of the navigation panel */
            left: 0;
            width: 100%;
            height: calc(100% - 60px);
            border: none;
        }

        #redeem-button {
            margin-left: auto;
            /* Push the redeem button to the right */
            padding: 5px 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        /* Add some spacing between the images and the redeem button */
        #navigation-panel img,
        #redeem-button {
            margin-right: 10px;
        }
    </style>
    <script>
        function loadProfilePage() {
            // Get the iframe element
            var iframe = document.getElementById('token-iframe');

            // Set the source URL of the iframe to profile.php
            iframe.src = 'profile.php';
        }

        function loadTokenPage() {
            // Get the iframe element
            var iframe = document.getElementById('token-iframe');

            // Set the source URL of the iframe to token.php
            iframe.src = 'token.php';
        }

        function loadRedeemPage() {
            // Get the iframe element
            var iframe = document.getElementById('token-iframe');

            // Set the source URL of the iframe to redeem.php
            iframe.src = 'redeem.php';
        }

        // Function to check if the user is logged in
        function isLoggedIn() {
            return '<?php echo isset($_SESSION["username"]) ? "true" : "false"; ?>';
        }
    </script>
</head>

<body>
    <div id="navigation-panel">
        <!-- Replace "Profile2.png" with the path to your profile image -->
        <img src="Profile2.png" alt="Profile Image" onclick="loadProfilePage()">

        <!-- Replace "Token.png" with the path to your token/QR code image -->
        <img src="Token.png" alt="Token/QR Code Image" onclick="loadTokenPage()">

        <!-- Add the redeem button -->
        <img id='navigation-panel-redeem' src="Redeem.jpg" alt="Redeem Image" onclick="loadRedeemPage()">
    </div>

    <!-- Iframe displaying token.php -->
    <iframe id="token-iframe" src="token.php"></iframe>
</body>

</html>