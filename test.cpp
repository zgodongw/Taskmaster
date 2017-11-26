/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.cpp                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: zgodongw <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/03 13:55:11 by zgodongw          #+#    #+#             */
/*   Updated: 2017/11/04 12:10:52 by zgodongw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <fstream>
#include <unistd.h>

int main(int ac, char **av)
{
	std::ofstream file;
	std::string line;

	if (ac < 2)
		line = "default Hello!";
	else
		line = (std::string)av[1];
	file.open("file.txt");
	for (int i = 0; i < 5; i++) {
		file << "Writing "<< line << std::endl;
		sleep(3);
	}
}
