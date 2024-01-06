//
//  WebSocket.swift
//  MacTell
//
//  Created by Yaroslav Korch on 06.01.2024.
//

import Foundation
import SwiftUI



class WebSocketManager: ObservableObject {
    var webSocketTask: URLSessionWebSocketTask?
    @Published var receivedMessage: UserServerInteractionData?
    var isConnected = false

    func connect() {
        if isConnected {
            return
        }

        let url = URL(string: "ws://localhost:8765")!
        webSocketTask = URLSession.shared.webSocketTask(with: url)
        webSocketTask?.resume()
        print("DEBUG: Connection established!")
        receiveMessage()
        isConnected = true
    }

    func disconnect() {
        webSocketTask?.cancel(with: .normalClosure, reason: nil)
    }

    func sendMessage(_ message: UserServerInteractionData) {
        if !(isConnected) {
            connect()
        }

        guard let jsonData = try? JSONEncoder().encode(message),
              let jsonString = String(data: jsonData, encoding: .utf8) else {
            print("ERROR: Failed to encode message")
            return
        }

        webSocketTask?.send(.string(jsonString)) { error in
            if let error = error {
                print("ERROR: WebSocket couldn’t send message because: \(error)")
            }
        }
    }

    private func receiveMessage() {

        webSocketTask?.receive { [weak self] result in
            switch result {
            case .failure(let error):
                print("Error in receiving message: \(error).        Or, the connection has been closed.")
            case .success(let message):
                switch message {
                case .string(let text):
                    DispatchQueue.main.async {
                        if let data = text.data(using: .utf8),
                           let message = try? JSONDecoder().decode(UserServerInteractionData.self, from: data) {
                            // Process the received message
                            self?.receivedMessage = message
                            // TODO: process the message
                        } else {
                            print("Failed to decode JSON")
                        }
                    }
                default:
                    break
                }
                self?.receiveMessage() // Continue listening for messages
            }
        }
    }
}
