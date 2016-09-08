/**
 * @Description Practice packet socket
 */

#include <sys/socket.h>
#include <linux/if_packet.h>
#include <net/ethernet.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <endian.h>

#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>

void checkError();
int getIfindex(int sockfd, const char* ifname);
int setPromiscuous(int sockfd, const char* ifname);
void shutdownSocket(int sig);
void help();


int sockfd = -1;
struct sigaction intAction = 
{
    .sa_handler = shutdownSocket,
};


void checkError()
{
    printf("ERROR: ioctl error %d(%s)\n", errno, strerror(errno));
}

int getIfindex(int sockfd, const char* ifname)
{
    struct ifreq req;
    strcpy(req.ifr_name, ifname);

    if(ioctl(sockfd, SIOCGIFINDEX, &req) != 0){
        checkError();
        return -1;
    }
    return req.ifr_ifindex;
}

int setPromiscuous(int sockfd, const char* ifname)
{
    struct ifreq req;
    strcpy(req.ifr_name, ifname);
    //req.ifr_flags &= ~IFF_PROMISC;
    req.ifr_flags |= IFF_PROMISC;

    if(ioctl(sockfd, SIOCSIFFLAGS, &req) < 0){
        checkError();
        return -1;
    }
    return 0;
}

void help()
{
    printf("Usage:\n    packet interface\n");
}

void shutdownSocket(int sig)
{
    if(sockfd > 0){
        close(sockfd);
        sockfd = -1;
    }
}

int main(int argc, char* argv[])
{
    if(argc < 2){
        help();
        return -1;
    }

    char *devName = argv[1];

    if(sigaction(SIGINT, &intAction, NULL) < 0){
        checkError();
        return -1;
    }

    sockfd = socket(AF_PACKET, SOCK_RAW, htole16(ETH_P_ALL));
    if(sockfd < 0){
        checkError();
        return -1;
    }
    //setPromiscuous(sockfd, devName);

    struct sockaddr_ll device;
    device.sll_family = AF_PACKET;
    device.sll_protocol = htole16(ETH_P_ALL);
    device.sll_ifindex = getIfindex(sockfd, devName);
    //device.sll_halen = 0;
    //device.sll_addr = 0;
    if(bind(sockfd, (struct sockaddr*)&device, sizeof(device)) < 0){
        checkError();
        return -1;
    }

    int len;
    unsigned char msg[2048];
    int cnt = 0;
    int addSpace = 0;

    while(sockfd > 0) {
        len = recvfrom(sockfd, msg, sizeof(msg), 0, NULL, NULL);
        if(len > 0){
            printf("[%d]", cnt);
            for(int i = 0; i < len; i++){
                if(msg[i] > '!' && msg[i] < '~'){
                    if(addSpace == 1){
                        printf(" %c", msg[i]);
                    }else{
                        printf("%c", msg[i]);
                    }
                    addSpace = 0;
                }else{
                    printf(" %.2x", msg[i]);
                    addSpace = 1;
                }
            }
            printf("\n");
            cnt++;
        }
    }

    printf("Exit...\n");
    return 0;
}
