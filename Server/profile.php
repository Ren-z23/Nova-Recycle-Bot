<!DOCTYPE html>
<html>
<head>
    <title>Profile Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }

        #profile-container {
            max-width: 600px;
            margin: 50px auto; /* Center the entire container horizontally */
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            text-align: center; /* Center the text content inside the container */
        }

        #profile-image {
            display: block;
            margin: 0 auto; /* Center the image horizontally */
            overflow: hidden; /* Hide any overflow caused by border-radius */
        }

        #username {
            font-size: 24px;
            font-weight: bold;
            margin: 20px 0;
        }

        #comment {
            text-align: center;
        }

        #back-button {
            text-align: center;
            margin-top: 20px;
        }

        #back-button button {
            font-size: 16px;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
    <script>
        function goBackToTokenPage() {
            // Navigate back to token.php by setting the iframe source
            window.parent.document.getElementById('token-iframe').src = 'token.php';
        }
    </script>
</head>
<body>
    <div id="profile-container">
        <h1>Profile</h1>
        <!-- Replace "profile_image.jpg" with the path to the user's profile image -->
        <img id="profile-image" src="Profile.png" alt="Profile Image">

        <?php
        session_start();

        // Check if the user is logged in and has a username in the session
        if (isset($_SESSION['username'])) {
            $username = $_SESSION['username'];
            // Replace "This is a sample comment" with the actual comment for the user
            $comment = "I am too overworked to finish this...";
        }
        ?>

        <div id="username"><?php echo $username; ?></div>
        <div id="comment"><?php echo $comment; ?></div>

        <!-- Back button to return to token.php -->
        <div id="back-button">
            <button onclick="goBackToTokenPage()">Back to Token Page</button>
        </div>
    </div>
</body>
</html>
