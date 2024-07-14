#include "base.cpp"

void setup_server(TCP::Socket *sock, int backlog = 10) {
    if (bind(sock->sockfd, sock->host->ai_addr, sock->host->ai_addrlen) == -1) {
        perror("Error binding to the server");
        exit(1);
    }

    if (listen(sock->sockfd, backlog) == -1) {
        perror("Error beginning to listen");
        exit(1);
    }
}

int accept_new_connection(TCP::Socket *sock) {
    sockaddr_storage addr;
    socklen_t addrlen;
    int new_fd = accept(sock->sockfd, (sockaddr *)&addr, &addrlen);
    if (new_fd == -1) {
        perror("Error accepting a new connection");
        return -1;
    }
    return new_fd;
}

void handle_connection(int clientfd, int serverfd, fd_set *fds, int fd_max) {
    char buff[4096];

    if (recv(clientfd, buff, sizeof buff, 0) <= 0) {
        close(clientfd);
        FD_CLR(clientfd, fds);
        return;
    }

    CHAT::Message *message;
    try {
        message = new CHAT::Message(buff);
    } catch (std::exception ex) {
        message = new CHAT::Message("server", "ERROR: Invalid request");
        if (send(clientfd, (void*) message->serialize().c_str(), 4096, 0) == -1) {
            perror("Error sending a message");
        }
        delete message;
        return;
    }

    printf("Sending message from %s.\n", message->username);
    std::string data = message->serialize();
    for (int i = 2; i < fd_max+1; i++) {
        if (FD_ISSET(i, fds) && i != clientfd && i != serverfd) {
            if (send(i, data.c_str(), 4096, 0) == -1) {
                perror("Error sending a message");
            }
        }
    }

    delete message;
}

int main(int argc, char** argv) {
    TCP::Socket *server_sock = new TCP::Socket(HOST, PORT);
    char buff[4096];
    setup_server(server_sock);

    fd_set masterfds, readyfds;
    FD_ZERO(&masterfds);
    FD_SET(server_sock->sockfd, &masterfds);
    int fd_max = server_sock->sockfd;

    printf("The server is running, accepting connections on %s:%s\n\n", HOST, PORT);

    while (1) {
        readyfds = masterfds;

        if (select(fd_max+1, &readyfds, NULL, NULL, NULL) == -1) {
            perror("select error");
            exit(1);
        }

        for (int fd = 0; fd < fd_max+1; fd++) {
            if (!FD_ISSET(fd, &readyfds))
                continue;
            
            if (fd == server_sock->sockfd) {
                int new_fd = accept_new_connection(server_sock);
                if (new_fd == -1) continue;
                if (new_fd > fd_max) fd_max = new_fd;
                FD_SET(new_fd, &masterfds);
            } else {
                handle_connection(fd, server_sock->sockfd, &masterfds, fd_max);
            }
        }
    }
}
