#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#include <cstdlib>
#include <cstring>
#include <cstdio>
#include <unistd.h>
#include <fcntl.h>

void execute_read(int sockfd) {
	char buff[4096];

	while (true) {
		memset(buff, 0, sizeof buff);
		if (recv(sockfd, buff, sizeof buff, 0) <= 0)
			break;

		printf("%s", buff);
	}
	printf("\n");
}

int main(int argc, char** argv) {
	if (argc != 4) {
		fprintf(stderr, "Wrong usage, use: gurl <url> <port> <file>\n");
		exit(1);
	}

	addrinfo hints, *host_addr;
	int status;
	char* hostname = argv[1];
	char* port = argv[2];
	char* file = argv[3];
	
	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	if ((status = getaddrinfo(hostname, port, &hints, &host_addr)) != 0) {
		perror("Error getting host information");
		exit(1);
	}

	int sockfd = socket(host_addr->ai_family, host_addr->ai_socktype, host_addr->ai_protocol);
	if ((status = connect(sockfd, host_addr->ai_addr, host_addr->ai_addrlen)) == -1) {
		perror("Error connecting to the server");
		exit(1);
	}

	char buff[4096];
	int fd = open(file, O_RDONLY);
	if (fd == -1) {
		perror("Error opening the file");
		exit(1);
	}

	int bytes_sent, bytes_read;
	while ((bytes_read = read(fd, buff, sizeof buff)) > 0) {
		char* ptr = buff;

		while (bytes_read > 0) {
			bytes_sent = send(sockfd, ptr, bytes_read, 0);
			if (bytes_sent <= 0) {
				perror("Error sending the file");
				close(fd);
				exit(1);
			}
			bytes_read -= bytes_sent;
			ptr += bytes_sent;
		}
	}

	execute_read(sockfd);
	return 0;
}
