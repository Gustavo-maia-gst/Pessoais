#include "base.cpp"
#include <fcntl.h>

void setup_client(TCP::Socket *sock) {
    if (connect(sock->sockfd, sock->host->ai_addr, sock->host->ai_addrlen) == -1) {
        perror("Error connecting to the server");
        exit(1);
    }
}

int main() {
    TCP::Socket *client_sock = new TCP::Socket(HOST, PORT);
    char username[50];
    char buff[4096];
    int status;

    setup_client(client_sock);

    printf("Hello, welcome to the open-chat! What's your name? ");
    fgets(username, sizeof username, stdin);
    for (int i = 0; i < sizeof username; i++) if (username[i] == '\n') username[i] = '\0';

    fd_set masterfds, readyfds;
    FD_ZERO(&masterfds);
    FD_SET(STDIN_FILENO, &masterfds);
    FD_SET(client_sock->sockfd, &masterfds);

    while (1) {
        readyfds = masterfds;

        if (select(client_sock->sockfd+1, &readyfds, NULL, NULL, NULL) == -1) {
            perror("select error");
            exit(1);
        }

        if (FD_ISSET(STDIN_FILENO, &readyfds)) {
            memset(buff, 0, sizeof buff);
            if (fgets(buff, sizeof buff, stdin) != NULL) {
                for (int i = 0; i < sizeof buff; i++) if (buff[i] == '\n') buff[i] = '\0';
                CHAT::Message message(username, buff);
                std::string text = message.serialize();
                if (send(client_sock->sockfd, text.c_str(), 4096, 0) <= 0) {
                    perror("Error sending the data: ");
                }
            }
        }

        if (FD_ISSET(client_sock->sockfd, &readyfds)) {
            memset(buff, 0, sizeof buff);
            if ((status = recv(client_sock->sockfd, buff, 4096, 0)) <= 0) {
                if (status == 0) continue;
                perror("Error reading from the socket");
            }
            CHAT::Message *message;
            try {
                message = new CHAT::Message(buff);
            } catch (std::exception ex) {
                delete message;
                continue;
            }
            printf("%s - <%s>\n%s\n\n", message->username, message->datestr, message->text);
            delete message;
        }
    }

    return 0;
}