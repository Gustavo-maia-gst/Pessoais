#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#include <cstdlib>
#include <cstring>
#include <cstdio>

char* gethostname(addrinfo *addr, char hostname[]) {
	void* s_addr;
	sockaddr_in *ip = (sockaddr_in *) addr->ai_addr;
	s_addr = &(ip->sin_addr);
	inet_ntop(AF_INET, s_addr, hostname, sizeof(hostname));
	return hostname;
}

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
	char* port = "8000";
	char hostname[INET6_ADDRSTRLEN];
	addrinfo hints, *host_addr;
	sockaddr_storage their_addr;
	socklen_t addr_size;
	int status;

	if (argc > 1)
		port = argv[1];
	
	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_flags = AI_PASSIVE;

	if ((status = getaddrinfo(NULL, port, &hints, &host_addr)) != 0) {
		perror("Error getting host information");
		exit(1);
	}

	int sockfd = socket(host_addr->ai_family, host_addr->ai_socktype, host_addr->ai_protocol);
	if ((status = bind(sockfd, host_addr->ai_addr, host_addr->ai_addrlen)) == -1) {
		perror("Error binding the server");
		exit(1);
	}
	if ((status = listen(sockfd, 10)) == -1) {
		perror("Error initializing the server");
		exit(1);
	}

	printf("The server is listening connections at: %s:%s\nPress Ctrl+C to shutdown the server\n\n", 
			gethostname(host_addr, hostname),
			port);

	while (true) {
		int tsockfd = accept(sockfd, (sockaddr *) &their_addr, &addr_size);
		execute_read(tsockfd);
	}

	return 0;
}
