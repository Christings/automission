<?php
	$file = "public.pem";//the public key file path
	$publicKey = openssl_get_publickey(file_get_contents($file));
	//$base64str = "nGS4ypnAH17Goonff/ZX22UsKUAfAWVVdw1Br1YkimsLvnFq/33Ddr4G3EAowTPwHOlOzIHBwDojFMbTXoVbNHDnFTKnq7FgL3JlLjGqSpPEDMcRY4aFn6tohHsmsQ0i7+X5G0Hr2wOoILoV7DuG1+bd9r/l8xq6akvTwjxebmjQWEpwJz5Aqs0kPk/9ThBMl9Htkbr25gJ6CD0E63/At3ZBE6eWkqDT6Eo/dPJNc5O/ZXtEmz4QsSJV02/adBrjyMQBQg+HXaGS1FwbkBs/+ZnZ5VZDo0kzeWH+Q2yUiKZq+uA6nRFnk2OEgpJ/UXRkT5vbG5HLeGra/UBdUNNNWA==";
    $base64str = $argv[1];
	$bcode = base64_decode($base64str);
	$sogou_user = "";
	openssl_public_decrypt($bcode,$sogou_user,$publicKey);
	echo $sogou_user;
?>
