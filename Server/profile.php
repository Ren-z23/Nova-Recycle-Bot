<?php
session_start();

// Check if the user is logged in and has a username in the session
if (isset($_SESSION['username'])) {
    $username = $_SESSION['username'];
    // Replace "This is a sample comment" with the actual comment for the user
    $comment = "I am too overworked to finish this...";
} else {
    // If the user is not logged in, redirect to index.php for login
    header('Location: index.php');
    exit;
}

// Handle logout action
if (isset($_POST['logout'])) {
    // Unset all session variables
    $_SESSION = array();

    // Destroy the session
    session_destroy();

    // Redirect the top-level window to index.php after logout
    echo '<script>window.top.location.href = "index.php";</script>';
    exit;
}
?>

<!-- Rest of the profile.php code remains the same -->


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
            margin: 50px auto;
            /* Center the entire container horizontally */
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            text-align: center;
            /* Center the text content inside the container */
        }

        #profile-image {
            display: block;
            margin: 0 auto;
            /* Center the image horizontally */
            overflow: hidden;
            /* Hide any overflow caused by border-radius */
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

        #logout-button {
            font-size: 16px;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
    </style>
    <script>
        function goBackToTokenPage() {
            // Navigate back to token.php by setting the iframe source
            window.parent.document.getElementById('token-iframe').src = 'token.php';
        }

        // Function to check if the user is logged in
        function isLoggedIn() {
            return '<?php echo isset($_SESSION["username"]) ? "true" : "false"; ?>';
        }

        // Function to handle logout
        function handleLogout() {
            // Redirect to index.php after logout
            window.location.href = 'index.php';
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

        <div id="username">
            <?php echo $username; ?>
        </div>
        <div id="comment">
            <?php echo $comment; ?>
        </div>

        <!-- Back button to return to token.php -->
        <div id="back-button">
            <button onclick="goBackToTokenPage()">Back to Token Page</button>
        </div>
    </div>
    <div id="back-button">
        <form method="post">
            <!-- Add the logout button -->
            <input type="submit" id="logout-button" name="logout" value="Logout">
    </div>
</body>

</html>