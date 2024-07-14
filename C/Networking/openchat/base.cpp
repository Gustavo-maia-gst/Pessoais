#include <stdexcept>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>

#define HOST "localhost"
#define PORT "8025"

typedef unsigned char byte;

namespace TCP {
    class Socket {
    public:
        int sockfd;
        addrinfo *host;

        Socket(char* hostname, char* port) {
            int yes = 1;

            host = this->gethost(hostname, port);
            for (; host != NULL; host = host->ai_next) {
                sockfd = socket(host->ai_family, host->ai_socktype, host->ai_protocol);
                if (sockfd == -1)
                    continue;

                setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof yes);
                break;
            }
            if (host == NULL) {
                perror("Error creating the socket");
                exit(1);
            }
        }

        Socket(int sockfd) {
            this->sockfd = sockfd;
            this->host = NULL;
        }

        static addrinfo* gethost(char* hostname, char* port) {
            addrinfo hints, *host;
            int status;

            memset(&hints, 0, sizeof hints);
            hints.ai_family = AF_UNSPEC;
            hints.ai_socktype = SOCK_STREAM;

            if ((status = getaddrinfo(hostname, port, &hints, &host)) != 0) {
                perror("Error obtaining host");
                exit(1);
            }

            return host;
        }

        ~Socket() {
            if (host != NULL)
                freeaddrinfo(host);

            close(sockfd);
        }
    };
}

namespace CHAT {
    class Message {
    public:
        char username[50];
        char text[1024];
        char datestr[50];
        tm *datetm;

        Message(char* request) {
            int readen = sscanf(request, "Username: %s\nDate: %s\nMessage: %[^\n]\n", &username, &datestr, &text);
            if (readen != 3) throw new std::exception();
        }

        Message(char* user, char* message_text) {
            memcpy(username, user, sizeof username);
            username[sizeof username - 1] = '\0';

            memcpy(text, message_text, sizeof text);
            text[sizeof text - 1] = '\0';

            time_t now; time(&now);
            datetm= localtime(&now);

            char date[50]; memset(date, 0, sizeof date);
            strftime(date, sizeof date, DATE_FORMAT, datetm);
            memcpy(datestr, date, 50);
        }

        std::string serialize() {
            time_t now; time(&now);
            datetm = localtime(&now);

            char date[50]; memset(date, 0, sizeof date);
            strftime(date, sizeof date, DATE_FORMAT, datetm);

            std::string str =  "Username: " + std::string(username) + "\n" +
                               "Date: " + std::string(date) + "\n" +
                               "Message: " + std::string(text) + "\n";
            
            return str;
        }
    private:
        const char* DATE_FORMAT = "%H:%M:%S-%d/%m/%Y";
    };
}
