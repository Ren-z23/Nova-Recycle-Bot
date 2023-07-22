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
            justify-content: space-between; /* Add this to space the images apart */
            align-items: center;
        }

        #navigation-panel img {
            height: 40px;
            cursor: pointer;
            border-radius: 50%; /* Make the profile image circular */
            overflow: hidden; /* Hide any overflow caused by border-radius */
        }

        #token-iframe {
            position: absolute;
            top: 60px; /* height of the navigation panel */
            left: 0;
            width: 100%;
            height: calc(100% - 60px);
            border: none;
        }

        /* Add this to create some space between the images */
        #navigation-panel img + img {
            margin-left: 10px;
        }
    </style>
    <script>
        function loadProfilePage() {
            // Get the iframe element
            var iframe = document.getElementById('token-iframe');

            // Set the source URL of the iframe to profile.php
            iframe.src = 'profile.php';
        }

        function loadRedeemPage() {
            // Get the iframe element
            var iframe = document.getElementById('token-iframe');

            // Set the source URL of the iframe to redeem.php
            iframe.src = 'redeem.php';
        }
    </script>
</head>
<body>
    <div id="navigation-panel">
        <!-- Replace "Profile2.png" with the path to your profile image -->
        <img src="Profile2.png" alt="Profile Image" onclick="loadProfilePage()">

        <!-- Replace "Redeem.png" with the path to your redeem image -->
        <img src="Redeem.jpg" alt="Redeem Image" onclick="loadRedeemPage()">
    </div>

    <!-- Iframe displaying token.php -->
    <iframe id="token-iframe" src="token.php"></iframe>
</body>
</html>
