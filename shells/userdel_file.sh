#!/bin/bash

input="user.dat"

while IFS=',' read -r username uid gid comment
do
	userdel -r "$username"
	echo "$username Deleted"
done < $input