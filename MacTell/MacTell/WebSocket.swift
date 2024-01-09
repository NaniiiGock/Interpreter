//
//  WebSocket.swift
//  MacTell
//
//  Created by Yaroslav Korch on 06.01.2024.
//

import Foundation

class WebSocketManager: ObservableObject {
    static let shared = WebSocketManager() // singleton

    var webSocketTask: URLSessionWebSocketTask?
    var onMessageReceived: ((UserServerInteractionData) -> Void)?
    var onPlethoraMessagesReceived: (([UserServerInteractionData]) -> Void)?

    func connect() {
        guard let url = URL(string: "ws://localhost:8765") else {
            fatalError("Invalid Socket URL")
        }

        webSocketTask = URLSession.shared.webSocketTask(with: url)
        webSocketTask?.resume()
        print("DEBUG: Connection established!")
        receiveMessage()
    }

    func disconnect() {
        webSocketTask?.cancel(with: .normalClosure, reason: nil)
    }

    func sendMessage(_ message: UserServerInteractionData) {
        guard let jsonData = try? JSONEncoder().encode(message),
              let jsonString = String(data: jsonData, encoding: .utf8)
        else {
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
                self?.processReceivedMessage(message)
            }
            self?.receiveMessage() // Continue listening for messages
        }
    }

    private func processReceivedMessage(_ message: URLSessionWebSocketTask.Message) {
        if case .string(let text) = message {
            DispatchQueue.main.async {
                if let data = text.data(using: .utf8) {
                    if let userServerInteractionData = try? JSONDecoder().decode(UserServerInteractionData.self, from: data) {
                        self.onMessageReceived?(userServerInteractionData)
                    } else if let aPlethoraOfBubbles = try? JSONDecoder().decode([UserServerInteractionData].self, from: data) {
                        self.onPlethoraMessagesReceived?(aPlethoraOfBubbles)
                    } else {
                        print("Failed to decode JSON")
                    }
                }
            }
        }
    }
}
